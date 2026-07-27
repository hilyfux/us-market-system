#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
outbox — 入队、两段式去重、可修订 report_key、路径可用性、抑制重复无变化报告

要点
  1. 路径可用性：outbox 必须在非 TCC 保护区。读写不到时抛
     EnqueuePathUnavailable，绝不退回 ~/Desktop（转发器读不到那里 = 静默丢消息）。
  2. 可修订键：report_key 永久幂等，但允许 `KEY#rN` 修订。旧设计下一份用降级数据
     发出的报告会永久烧掉该键，之后无法重发更正版。
  3. 抑制重复：内容指纹相同且无风险标记时不重复推送，治理告警疲劳
     （旧设计一天可推 ~16 条，多数是同一句「持有 + 降级」）。
"""
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from report_lint import lint_report, stage_from_report_key, ReportLintError

DEFAULT_OUTBOX = "/Users/linqing.wang/.local/share/us-stock-outbox"
TCC_PROTECTED_PREFIXES = ("/Users/linqing.wang/Desktop", "/Users/linqing.wang/Documents",
                          "/Users/linqing.wang/Downloads")
ALLOWED_WEBHOOK_HOST = "qyapi.weixin.qq.com"
REVISION_RE = re.compile(r"^(?P<base>.+?)(?:#r(?P<rev>\d+))?$")


class EnqueuePathUnavailable(RuntimeError):
    pass


class TccProtectedPath(RuntimeError):
    pass


def outbox_path() -> str:
    """
    宿主机（launchd 转发器、agent 的文件工具）使用 DEFAULT_OUTBOX。
    代码执行沙箱看到的是挂载路径，两者文件系统命名空间不同，
    因此在沙箱内运行本库时必须显式设置 US_STOCK_OUTBOX。
    刻意不做自动回退 —— 静默换路径正是本次事故（消息只入队不投递）的成因。
    """
    return os.environ.get("US_STOCK_OUTBOX", DEFAULT_OUTBOX)


ANCHOR_NAME = ".anchor"
ANCHOR_CONTENT = "us-stock-outbox v1"


def assert_path_usable(path: Optional[str] = None, create_anchor: bool = False) -> str:
    """
    2026-07-27 新增**锚定哨兵**：真 outbox 必须含 `.anchor` 文件（内容固定）。

    背景（实测确认的静默丢失陷阱）：沙箱内 `~` 解析为沙箱 home，而非宿主机 home。
    若运行照抄 `US_STOCK_OUTBOX=~/.local/share/us-stock-outbox`，旧实现会在沙箱 home
    **新建一个空 outbox 并通过检查**——消息入队到转发器永远不看的目录 = 静默丢失，
    正是 §5 要杜绝的事故类别。故：目录不存在或缺锚定文件 → 一律 EnqueuePathUnavailable；
    绝不静默创建生产 outbox。`create_anchor=True` 仅供测试/显式初始化使用。
    """
    p = path or outbox_path()
    for pref in TCC_PROTECTED_PREFIXES:
        if os.path.abspath(p).startswith(pref):
            raise TccProtectedPath(
                "outbox 位于 TCC 保护区 %s；launchd 后台转发器无法读取，"
                "会造成消息只入队不投递。请使用 ~/.local/share/us-stock-outbox。" % pref)
    anchor = os.path.join(p, ANCHOR_NAME)
    if create_anchor:
        os.makedirs(p, exist_ok=True)
        if not os.path.exists(anchor):
            with open(anchor, "w", encoding="utf-8") as f:
                f.write(ANCHOR_CONTENT)
    if not os.path.isdir(p):
        raise EnqueuePathUnavailable(
            "outbox %s 不存在。拒绝自动创建（防沙箱 home 假 outbox 静默吞消息）；"
            "请确认挂载与路径，或显式初始化后重试。" % p)
    try:
        with open(anchor, encoding="utf-8") as f:
            first = f.readline().strip()
        if first != ANCHOR_CONTENT:
            raise OSError("锚定文件内容不符：%r" % first)
    except OSError as e:
        raise EnqueuePathUnavailable(
            "outbox %s 缺少有效锚定文件 %s（%s）。该目录可能是错误路径上被误建的空 outbox"
            "（如沙箱 home），消息写入将被静默丢弃 -> 按 ENQUEUE_PATH_UNAVAILABLE 处理。"
            % (p, ANCHOR_NAME, e))
    # 探针只验证 enqueue() 真正依赖的能力：建目录 + 原子写(tmp -> rename) + 读回。
    # 2026-07-27 修正：旧探针用 write-then-`os.remove`，把 unlink 当作可用性硬条件。
    # 但 enqueue() 从不 unlink——它只 write .tmp 再 os.rename 成 .json；消息的归档/删除
    # 由宿主机 launchd 转发器完成（那侧 unlink 正常）。部分沙箱 FUSE 挂载允许
    # open/write/rename 却拒绝 unlink（EPERM，[Errno 1] Operation not permitted），
    # 旧探针因此在 outbox 实际可用时误报 ENQUEUE_PATH_UNAVAILABLE，间歇性阻断健康运行
    # （含可交易的 MORNING/PREMARKET）。故：write / rename / read-back 失败 = 致命；
    # unlink（仅用于清理探针）失败 = 非致命，尽力而为。
    tmp = os.path.join(p, ".writeprobe.tmp")
    # 终名为点文件且**非 .json**：不会被 queue_state()/转发器误当成待投递消息。
    final = os.path.join(p, ".writeprobe")
    token = "ok-%d" % os.getpid()
    try:
        os.makedirs(p, exist_ok=True)
        for sub in ("sent", "failed", ".attempts"):
            os.makedirs(os.path.join(p, sub), exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(token)
        os.rename(tmp, final)          # 这正是 enqueue() 的原子入队动作
        with open(final, encoding="utf-8") as f:
            if f.read() != token:
                raise OSError("probe read-back 不一致：outbox 写入不可信")
    except OSError as e:
        raise EnqueuePathUnavailable(
            "outbox %s 不可读写（%s）。按 SYSTEM.md §5 应记 ENQUEUE_PATH_UNAVAILABLE 并结束，"
            "不得改写到别处。" % (p, e))
    # 清理探针：部分挂载拒绝 unlink（EPERM）属已知无害现象，绝不因此判 outbox 不可用。
    for junk in (tmp, final):
        try:
            os.remove(junk)
        except OSError:
            pass
    return p


def parse_key(report_key: str) -> Tuple[str, int]:
    m = REVISION_RE.match(report_key)
    return m.group("base"), int(m.group("rev") or 0)


def delivered_keys(path: Optional[str] = None) -> List[str]:
    p = os.path.join(path or outbox_path(), ".delivered-keys")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def _queued_keys(p: str) -> List[str]:
    out = []
    for d in (p, os.path.join(p, "sent"), os.path.join(p, "failed")):
        if not os.path.isdir(d):
            continue
        for n in os.listdir(d):
            if n.endswith(".json"):
                out.append(re.sub(r"^\d{8}-\d{6}_", "", n[:-5]))
    return out


def is_duplicate(report_key: str, alert_state_keys: List[str], path: Optional[str] = None) -> Tuple[bool, str]:
    """入队前查重：alert-state（已确认送达）+ outbox 根/sent/failed（已入队或在途）。"""
    p = path or outbox_path()
    if report_key in alert_state_keys:
        return True, "已在 alert-state（已确认送达）"
    if report_key in delivered_keys(p):
        return True, "已在 .delivered-keys（转发器已确认 errcode=0）"
    if report_key in _queued_keys(p):
        return True, "已存在于 outbox（已入队或在途）"
    return False, ""


def next_revision(base_key: str, path: Optional[str] = None) -> str:
    """为已烧掉的键生成下一个修订号，用于重发更正版报告。"""
    p = path or outbox_path()
    seen = set(delivered_keys(p)) | set(_queued_keys(p))
    rev = 0
    for k in seen:
        b, r = parse_key(k)
        if b == base_key:
            rev = max(rev, r)
    return "%s#r%d" % (base_key, rev + 1)


def content_fingerprint(markdown: str) -> str:
    """内容指纹：忽略时间戳行，用于抑制重复的无变化报告。"""
    lines = [ln for ln in markdown.splitlines()
             if not re.search(r"\d{4}-\d{2}-\d{2}T?\d{0,2}:?\d{0,2}", ln)]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:16]


def should_suppress(fingerprint: str, path: Optional[str] = None,
                    has_risk_flag: bool = False, force: bool = False) -> Tuple[bool, str]:
    """
    与上一条同阶段报告内容指纹相同、且无风险标记时抑制。
    风险标记（🚨）或 force 一律放行——安全信息绝不被抑制。
    """
    if force or has_risk_flag:
        return False, ""
    p = os.path.join(path or outbox_path(), ".last-fingerprint")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            if f.read().strip() == fingerprint:
                return True, "内容与上一条同阶段报告完全一致且无风险标记 -> 抑制以避免告警疲劳"
    return False, ""


def _record_fingerprint(fingerprint: str, p: str) -> None:
    with open(os.path.join(p, ".last-fingerprint"), "w", encoding="utf-8") as f:
        f.write(fingerprint)


def enqueue(report_key: str, markdown: str, webhook: str,
            path: Optional[str] = None, has_risk_flag: bool = False,
            force: bool = False, alert_state_keys: Optional[List[str]] = None,
            lint: bool = True) -> Dict[str, object]:
    """
    原子入队（先 .tmp 再 rename）。返回 {enqueued, reason, file, report_key, fingerprint}

    lint=True（默认）：阶段报告入队前先过 SYSTEM.md §5 可读性/无歧义硬门，
    不合格抛 ReportLintError（响亮失败，修正后用 KEY#rN 重发），绝不静默推送歧义报告。
    仅对阶段键（PREMARKET/INTRADAY/MORNING/POSTCLOSE）生效；SIMTEST/SELFTEST 等非阶段键跳过。
    测试机制（去重/抑制）用 lint=False。
    """
    p = assert_path_usable(path)
    if not webhook or ALLOWED_WEBHOOK_HOST not in webhook:
        raise ValueError("webhook 主机必须是 %s；当前值被拒绝（防止把内容发到错误端点）"
                         % ALLOWED_WEBHOOK_HOST)

    if lint:
        stage = stage_from_report_key(report_key)
        if stage is not None:
            res = lint_report(markdown, stage)
            if not res["ok"]:
                raise ReportLintError(res["violations"])

    dup, why = is_duplicate(report_key, alert_state_keys or [], p)
    if dup:
        return {"enqueued": False, "reason": "DUPLICATE: " + why, "report_key": report_key}

    fp = content_fingerprint(markdown)
    sup, swhy = should_suppress(fp, p, has_risk_flag, force)
    if sup:
        return {"enqueued": False, "reason": "SUPPRESSED: " + swhy,
                "report_key": report_key, "fingerprint": fp}

    payload = {
        "report_key": report_key,
        "created_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "webhook": webhook,
        "payload": {"msgtype": "markdown", "markdown": {"content": markdown}},
    }
    tmp = os.path.join(p, report_key.replace("#", "__") + ".tmp")
    final = os.path.join(p, report_key.replace("#", "__") + ".json")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    os.rename(tmp, final)
    _record_fingerprint(fp, p)
    return {"enqueued": True, "reason": "OK", "file": final,
            "report_key": report_key, "fingerprint": fp}


def queue_state(path: Optional[str] = None) -> Dict[str, object]:
    """给 health 检查用：待投递、死信、最旧待投递年龄。"""
    p = path or outbox_path()
    if not os.path.isdir(p):
        return {"pending": [], "failed": [], "oldest_pending_age_min": None, "available": False}
    pending = [n for n in os.listdir(p) if n.endswith(".json")]
    failed_dir = os.path.join(p, "failed")
    # 死信只数真正的消息文件（.json 且是文件），与 pending 口径一致：
    # 探针/清理残留的点文件（如 .wp）或归档子目录（failed/archive/）不得被误当成死信，
    # 否则会像 unlink 误报一样制造假 W3 升级（2026-07-27）。
    failed = ([n for n in os.listdir(failed_dir)
               if n.endswith(".json") and os.path.isfile(os.path.join(failed_dir, n))]
              if os.path.isdir(failed_dir) else [])
    oldest = None
    if pending:
        now = time.time()
        oldest = max((now - os.path.getmtime(os.path.join(p, n))) / 60.0 for n in pending)
    return {"pending": pending, "failed": failed,
            "oldest_pending_age_min": oldest, "available": True}


def reconcile_delivered_to_alert_state(alert_state_keys: List[str],
                                       path: Optional[str] = None) -> List[str]:
    """
    返回需要写入 alert-state 的新确认键。
    SIMTEST-/SELFTEST- 前缀不是阶段 report_key，刻意排除。
    """
    out = []
    for k in delivered_keys(path):
        if k.startswith(("SIMTEST-", "SELFTEST-", "PIPELINE-")):
            continue
        if k not in alert_state_keys:
            out.append(k)
    return out
