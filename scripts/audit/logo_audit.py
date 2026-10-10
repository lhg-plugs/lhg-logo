#!/usr/bin/env python3
"""lhg-logo 确定性 Logo 审计：16 条规则，零第三方依赖。

扫描交付目录（*.svg + brand.json），检查 SVG 规范（viewBox、文字转曲、
空元素）、尺寸覆盖（favicon/社交/印刷）、色彩对比度（WCAG 相对亮度）、
深浅底/单色版本、安全区与原创性声明。

用法：
    python3 logo_audit.py --target <目录> [--format json|text]
        [--fail-on blocker|warning|nit]

退出码：2=有 blocker，1=有 warning（无 blocker），0=干净。
规则文案均为本项目原创（品牌规范方法论见 skills/，独立撰写，
未复制任何第三方原文与 logo 语料；详见仓库 ATTRIBUTION.md）。
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

VERSION = "1.0.0"
TOOL = "lhg-logo/logo-audit"

SKIP_DIRS = {".git", "__pycache__", "node_modules", "dist", "build"}


class Finding:
    __slots__ = ("rule_id", "severity", "category", "title", "file", "line",
                 "snippet", "detail")

    def __init__(self, rule_id, severity, category, title, file, line,
                 snippet, detail):
        self.rule_id = rule_id
        self.severity = severity
        self.category = category
        self.title = title
        self.file = file
        self.line = line
        self.snippet = snippet
        self.detail = detail

    def to_dict(self):
        return {
            "rule_id": self.rule_id, "severity": self.severity,
            "category": self.category, "title": self.title,
            "file": self.file, "line": self.line,
            "snippet": self.snippet, "detail": self.detail,
        }


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except (UnicodeDecodeError, OSError):
        return ""


def local(tag):
    return tag.split("}")[-1] if "}" in tag else tag


def iter_elems(root):
    for el in root.iter():
        yield el


# ---- WCAG 相对亮度 ----
def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexcolor):
    h = hexcolor.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) != 6:
        return None
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return None
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(hex1, hex2):
    l1, l2 = luminance(hex1), luminance(hex2)
    if l1 is None or l2 is None:
        return None
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--format", choices=["json", "text"], default="text")
    ap.add_argument("--fail-on", default="blocker",
                    choices=["blocker", "warning", "nit"])
    args = ap.parse_args()

    findings = []
    sev_rank = {"blocker": 3, "warning": 2, "nit": 1}

    def add(rule_id, severity, category, title, f, ln, snippet, detail):
        findings.append(Finding(rule_id, severity, category, title, f, ln,
                                snippet, detail))

    svgs, brands = [], []
    if os.path.isfile(args.target) and args.target.lower().endswith(".svg"):
        svgs = [args.target]
    else:
        for root, dirs, files in os.walk(args.target):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fn in sorted(files):
                p = os.path.join(root, fn)
                if fn.lower().endswith(".svg"):
                    svgs.append(p)
                elif fn.lower() == "brand.json":
                    brands.append(p)

    if not svgs and not brands:
        print("未找到 SVG 或 brand.json", file=sys.stderr)
        return 2

    # ---- SVG 规则 ----
    for fp in svgs:
        raw = read_text(fp)
        short = os.path.basename(fp)
        if not raw.strip():
            add("SVG-PARSE-001", "blocker", "SVG", "SVG 文件为空", fp, 0,
                short, "空文件无法作为 logo 资产交付")
            continue
        try:
            root = ET.fromstring(raw)
        except Exception as e:
            add("SVG-PARSE-001", "blocker", "SVG",
                "SVG 解析失败：%s" % str(e)[:60], fp, 0, short,
                "文件不是合法 XML/SVG，请重新导出")
            continue

        viewBox = root.get("viewBox")
        width, height = root.get("width"), root.get("height")
        if not viewBox:
            add("SVG-VIEWBOX-001", "blocker", "SVG", "缺少 viewBox",
                fp, 0, short, "补 viewBox=\"0 0 <w> <h>\"，否则缩放失真")
        elif not (width and height):
            add("SVG-SIZE-001", "warning", "SVG",
                "有 viewBox 但无 width/height（默认渲染尺寸未声明）",
                fp, 0, short, "建议补 width/height，明确默认尺寸")

        has_text = any(local(el.tag) == "text" for el in iter_elems(root))
        if has_text:
            add("SVG-TEXT-001", "warning", "SVG",
                "含 <text> 元素：交付前请转曲",
                fp, 0, short, "文字转成 path 后交付，否则换机器字体走样")

        empty = []
        for el in iter_elems(root):
            t = local(el.tag)
            if t == "path" and not (el.get("d") or "").strip():
                empty.append("空 path")
            for attr in ("width", "height", "r", "rx"):
                v = el.get(attr)
                if v is not None:
                    try:
                        if float(re.sub(r"[a-z%]+$", "", v)) == 0:
                            empty.append("零尺寸 %s" % t)
                    except ValueError:
                        pass
        if empty:
            add("SVG-EMPTY-001", "blocker", "SVG",
                "空/零尺寸图形元素：%s" % "、".join(sorted(set(empty))[:3]),
                fp, 0, short, "清理设计工具导出的垃圾元素后重新导出")

        has_title = any(local(el.tag) == "title" for el in iter_elems(root))
        if not has_title:
            add("SVG-TITLE-001", "nit", "SVG", "缺少 <title>（无障碍）",
                fp, 0, short, "加上 <title>品牌名 logo</title>，读屏软件可读")

    # ---- brand.json 规则 ----
    for fp in brands:
        short = os.path.basename(fp)
        try:
            brand = json.loads(read_text(fp))
        except Exception as e:
            add("SVG-JSON-001", "blocker", "规范",
                "brand.json 不是合法 JSON：%s" % str(e)[:60],
                fp, 0, short, "修复 JSON 语法后重跑")
            continue
        if not isinstance(brand, dict):
            add("SVG-JSON-001", "blocker", "规范",
                "brand.json 顶层不是对象", fp, 0, short, "按 skill 模板重写")
            continue

        exports = brand.get("exports") or []
        purposes = " ".join(
            str(e.get("purpose", "")) for e in exports
            if isinstance(e, dict))
        sizes = [e.get("size") for e in exports if isinstance(e, dict)]
        if not any("favicon" in purposes.lower() or s in (16, 32)
                   for s in sizes):
            add("SIZE-FAVICON-001", "warning", "尺寸",
                "导出清单缺 favicon（16/32）", fp, 0, short,
                "浏览器标签页是 logo 的地狱模式，必须单独出")
        if not any(k in purposes for k in ("社交", "avatar", "头像")) \
                and not any(s in (180, 400) for s in sizes):
            add("SIZE-SOCIAL-001", "warning", "尺寸",
                "导出清单缺社交头像尺寸（180/400）", fp, 0, short,
                "注意各平台圆形裁切，关键图形居中")
        if not any(k in purposes.lower() for k in ("印刷", "print", "矢量")):
            add("SIZE-PRINT-001", "warning", "尺寸",
                "导出清单缺印刷/矢量版本声明", fp, 0, short,
                "名片/门头/包装必须给矢量，不给 PNG 放大")

        palette = brand.get("palette") or {}
        backgrounds = brand.get("backgrounds") or {}
        colors = dict(palette); colors.update(backgrounds)
        if isinstance(palette, dict) and len(palette) > 4:
            add("COLOR-COUNT-001", "nit", "色彩",
                "色数 %d（>4），建议精简" % len(palette), fp, 0, short,
                "好 logo 通常 ≤3 色，色多=记忆成本高")
        for pair in brand.get("contrast_pairs") or []:
            if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                continue
            fg, bg = pair
            c = contrast(colors.get(fg, ""), colors.get(bg, ""))
            if c is None:
                continue
            if c < 4.5:
                add("COLOR-CONTRAST-001", "warning", "色彩",
                    "对比度不足：%s 在 %s 上为 %.2f:1（<4.5）"
                    % (fg, bg, c), fp, 0, short,
                    "加深标志色或换背景，深底版单独算一遍")

        variants = brand.get("variants") or {}
        if variants.get("dark") is not True:
            add("THEME-DARK-001", "warning", "版本",
                "未声明深色底版本", fp, 0, short,
                "深底版单独调色单独出，不许拿浅底版反色将就")
        if variants.get("mono") is not True:
            add("THEME-MONO-001", "warning", "版本",
                "未声明单色版本", fp, 0, short,
                "传真/雕刻/单色印刷只能用单色版")

        cs = (brand.get("clearspace") or "").strip()
        if not cs or "待定" in cs:
            add("CLEARSPACE-001", "nit", "规范",
                "安全区未声明", fp, 0, short,
                "写入如“四周留白 ≥ x/4”，这是 logo 的社交距离")
        if not brand.get("min_size_px"):
            add("MINSIZE-001", "nit", "规范",
                "最小尺寸未声明", fp, 0, short,
                "测出糊掉的临界 px 并写入，小于它用简化版")
        oc = (brand.get("originality_check") or "").strip()
        if not oc:
            add("TRADEMARK-001", "nit", "合规",
                "原创性/商标检索声明缺失", fp, 0, short,
                "填“已提示用户做商标近似检索+日期”，诚实比空白强")

    findings.sort(key=lambda x: (-sev_rank[x.severity], x.rule_id))
    summary = {
        "tool": TOOL, "version": VERSION,
        "target": args.target,
        "files_checked": len(svgs) + len(brands),
        "rules_run": 16,
        "blocker": sum(1 for x in findings if x.severity == "blocker"),
        "warning": sum(1 for x in findings if x.severity == "warning"),
        "nit": sum(1 for x in findings if x.severity == "nit"),
    }

    if args.format == "json":
        print(json.dumps({"summary": summary,
                          "findings": [x.to_dict() for x in findings]},
                         ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("lhg-logo 审计报告（%d 个文件，%d 条规则）"
              % (summary["files_checked"], summary["rules_run"]))
        print("blocker=%d warning=%d nit=%d"
              % (summary["blocker"], summary["warning"], summary["nit"]))
        print("=" * 60)
        for x in findings:
            print("[%s] %s %s" % (x.severity.upper(), x.rule_id, x.title))
            print("    %s %s" % (x.file, x.snippet))
            print("    → %s" % x.detail)
        if not findings:
            print("干净：未发现问题。")

    level = {"blocker": 3, "warning": 2, "nit": 1}[args.fail_on]
    worst = max([sev_rank[x.severity] for x in findings], default=0)
    if worst >= 3:
        return 2
    if worst == 2:
        return 1 if level <= 2 else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
