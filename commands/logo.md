---
description: 品牌简介→设计简报→3 版概念→几何规范→SVG 源文件→导出清单→应用自检，端到端交付 logo 资产包。
argument-hint: [品牌一句话简介] [--scene app]
---

# /lhg-logo:logo —— 一句话出 logo 资产包

用户输入在 `$ARGUMENTS` 中：`[品牌一句话简介] [--scene 主场景]`。主场景缺省 `social`（社交媒体）。

全程加载 `lhg-logo-brief` → `lhg-logo-concept` → `lhg-logo-geometry` → `lhg-logo-export`。设计工作可分派给 `brand-designer` agent，定稿前必须走 `logo-audit` 与 `logo-critique`。

## 流程

### 1. 简报（加载 lhg-logo-brief）
- 按"简报五问"访谈，最多问两轮；输出 `brief.md` + `brand.json`，**用户确认后才往下走**。
- 简报没确认就画图 → 不许。

### 2. 概念（加载 lhg-logo-concept）
- 三方向法出 3 个概念（字母/图形/组合各一），写 `concepts.md`（一句话 idea + 诚实风险）。
- 用户选定 1 个方向（用 4.5 取舍指南辅助决策）。

### 3. 几何规范（加载 lhg-logo-geometry）
- 网格构建 → 安全区 → 最小尺寸 → 单色版 → 深浅底适配，输出 `spec.md` + `logo.svg` 系列源文件。
- 文字必须转曲（交付文件不许留 `<text>`）。

### 4. 导出与自检（加载 lhg-logo-export）
- 按导出清单生成 `delivery/`（favicon/社交/APP/官网/印刷/深色/单色）。
- 跑 `/lhg-logo:logo-audit`，blocker 清零；做应用场景走查（16px/圆切/深色/单色/远距离/竞品并排）。

### 5. 交付
- 交付 `delivery/` + `spec.md` + `concepts.md` + `brief.md`（四件套）。
- **导出交付前 hook 会自动校验 SVG 规范**（见 hooks 说明）。被拦截就修 SVG，不要关 hook。

## 硬规则
- 简报没确认就出概念 → 不许。
- 临摹/描摹任何现有 logo → 不许（原创性红线）。
- 承诺"商标一定能注册" → 不许；正式使用前建议专业商标检索（见 logo-critique）。
- 为通过自检改审计脚本规则 → 作弊，不许。
