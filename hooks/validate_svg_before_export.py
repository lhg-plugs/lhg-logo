#!/usr/bin/env python3
"""lhg-logo 硬门：导出/交付 logo 前校验 SVG 规范。

触发：PreToolUse / Bash。脚本先判断本次 Bash 命令是否为"导出意图"
（命令含 export/deliver/kit 且目标含 .svg/.png，或调用 logo-kit），
不是则 0 开销直接放行；是则校验当前目录下（及 delivery/ 子目录）的
SVG 文件。

校验项：SVG 可解析、非空、有 viewBox、无空 path/零尺寸元素。
<text> 未转曲只做提醒（warning），不拦截——设计稿阶段允许用文字。

逃生方式（按推荐度排序）：
  1. 修好 SVG 后重新导出（推荐）。
  2. 紧急情况：LHG_LOGO_HOOKS_OFF=1 <导出命令>（单次豁免本次 hook）。
  3. /plugin disable lhg-logo（整个插件停用，hooks 不再触发）。

设计原则：脚本内部出错（找不到 SVG、解析异常等）时 fail-open
直接放行，不因插件自身故障骚扰用户；真正的门禁在
/lhg-logo:logo-audit。找不到 SVG 文件时直接放行（可能与本插件无关）。
零第三方依赖。
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET

EXPORT_RE = re.compile(
    r"(?<![\w-])(export|deliver|logo-kit|render-logo)\b.*\.(svg|png)\b"
    r"|\blogo-kit\b",
    re.I,
)


def find_svgs(project_dir):
    found = []
    for base in (project_dir, os.path.join(project_dir, "delivery")):
        if not os.path.isdir(base):
            continue
        try:
            for fn in os.listdir(base):
                if fn.lower().endswith(".svg"):
                    found.append(os.path.join(base, fn))
        except OSError:
            pass
    return found


def local(tag):
    return tag.split("}")[-1] if "}" in tag else tag


def validate_svg(path):
    """返回 (ok, [问题列表])。"""
    problems = []
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as e:
        return False, ["读文件失败：%s" % e]
    if not raw.strip():
        return False, ["SVG 文件为空"]
    try:
        root = ET.fromstring(raw)
    except Exception as e:
        return False, ["SVG 解析失败：%s" % str(e)[:80]]
    if not root.get("viewBox"):
        problems.append("缺少 viewBox（缩放会失真）")
    for el in root.iter():
        t = local(el.tag)
        if t == "path" and not (el.get("d") or "").strip():
            problems.append("存在空 path 元素")
            break
    for el in root.iter():
        t = local(el.tag)
        for attr in ("width", "height", "r"):
            v = el.get(attr)
            if v is not None:
                try:
                    if float(re.sub(r"[a-z%]+$", "", v)) == 0:
                        problems.append(
                            "存在零尺寸图形元素 <%s %s=0>" % (t, attr))
                        raise StopIteration
                except (ValueError, StopIteration):
                    break
        else:
            continue
        break
    return (not problems), problems


def main() -> int:
    # 逃生开关
    if os.environ.get("LHG_LOGO_HOOKS_OFF") == "1":
        return 0

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0  # 输入解析失败：fail-open

    tool_input = payload.get("tool_input", {}) or {}
    command = tool_input.get("command", "") or ""

    # 非导出命令：快速放行
    if not EXPORT_RE.search(command):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    svgs = find_svgs(project_dir)

    if not svgs:
        return 0  # 找不到 SVG：直接放行（可能与本插件无关）

    try:
        results = [(p, validate_svg(p)) for p in svgs]
    except Exception:
        return 0  # 校验自身出错：fail-open

    bad = [(p, ps) for p, (ok, ps) in results if not ok]
    if not bad:
        return 0

    lines = [
        "导出被 lhg-logo 硬门拦截：SVG 校验发现 %d 个文件有问题，修好再导出。"
        % len(bad),
        "",
    ]
    for p, ps in bad[:5]:
        lines.append("- %s" % os.path.basename(p))
        for pr in ps[:3]:
            lines.append("    · " + pr)
    lines += [
        "",
        "修复方式：按 lhg-logo-geometry 第 4 节 SVG 规范修正后重新导出；",
        "紧急豁免（单次）：LHG_LOGO_HOOKS_OFF=1 <导出命令>",
    ]
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "\n".join(lines),
        }
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
