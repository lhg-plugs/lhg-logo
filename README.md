<!-- About 简介（推送后填写到仓库 About 栏）：
Logo设计专家：品牌简介→多版概念→几何规范→多尺寸导出清单→应用场景自检，SVG 确定性审计全程护航。 ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-logo
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, logo, branding, identity, svg, design -->

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="lhg-logo — Logo设计专家">
</p>

> **一句话介绍**：Logo设计专家：品牌简介→多版概念→几何规范→多尺寸导出清单→应用场景自检，SVG 确定性审计全程护航。

**一键安装**：在 Claude Code 里运行

```bash
/plugin marketplace add lhg-plugs/lhg-logo
/plugin install lhg-logo@lhg-plugs
```

## 它能帮你做出什么

- **冒烟全绿**：`python3 smoke_test.py` 51 项全部通过（JSON 合法、frontmatter 完整、命令/skill/agent 齐全）。

## 它是什么

`lhg-logo` 是一个 Claude Code 插件（plugin 为主、skill 为辅）：

- **4 个命令**（小白入口）：`logo` 品牌简介→设计简报→3 版概念→几何规范、`logo-audit` Logo 确定性审计、`logo-critique` 概念评审、`logo-kit` 已有 logo.svg → 生成多尺寸导
- **4 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等 agent 平台）：lhg-logo-brief, lhg-logo-concept, lhg-logo-export, lhg-logo-geometry
- **3 个专家 agent**：brand-designer, originality-reviewer, spec-auditor
- **1 个 hooks**（`hooks/`：validate_svg_before_export.py），关键操作前自动把关

## 为什么是它

不是一个 prompt，而是一套互相兜底的机制：

1. **硬门，不是提醒**：hooks 在关键操作前自动拦截或警告（见 `hooks/`），而不是只在文档里写一句"请注意"。
2. **方法论沉淀在 skill 里**：流程、检查清单、口径都写在 `skills/` 的方法论里，命令只是入口；换个 agent 平台也能复用同一套做法。
3. **可验，不是可信**：`fixtures/` 备有坏/好对照用例，`smoke_test.py` 一键验证，规则有没有生效、自己跑一遍就知道。

## 快速上手

```bash
# 1. 安装（Claude Code 里运行）
/plugin marketplace add lhg-plugs/lhg-logo
/plugin install lhg-logo@lhg-plugs

# 2. 品牌简介→设计简报→3 版概念→几何规范→SVG 源文件→导出清单→应用自检，端
/lhg-logo:logo "社区咖啡店，主打手冲" --scene social
```

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-logo:logo` | 品牌简介→设计简报→3 版概念→几何规范→SVG 源文件→导出清单→应用自检，端到端交付 logo 资产包。 | `/lhg-logo:logo "社区咖啡店，主打手冲" --scene social` |
| `/lhg-logo:logo-audit` | Logo 确定性审计：SVG 规范（viewBox/文字转曲/空元素）+ 尺寸覆盖 + 色彩对比度 + 深浅底/单色版本… | `/lhg-logo:logo-audit ./delivery/` |
| `/lhg-logo:logo-critique` | 概念评审：原创性审查（避让清单比对）+ 商标风险提示 + 16px/单色/深底三项生存测试，不许承诺商标结果。 | `/lhg-logo:logo-critique ./concepts.md` |
| `/lhg-logo:logo-kit` | 已有 logo.svg → 生成多尺寸导出包（favicon/社交/APP/印刷/深浅底/单色）+ 命名规范 + CHE… | `/lhg-logo:logo-kit ./logo.svg --out ./delivery/` |

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用：**

- 你需要品牌简介→设计简报→3 版概念→几何规范→SVG时 → 用 `/lhg-logo:logo`
- 你需要Logo 确定性审计时 → 用 `/lhg-logo:logo-audit`
- 你需要概念评审时 → 用 `/lhg-logo:logo-critique`

**什么时候不用：**

- 你只需要其中一个零散能力时 → 本插件是成套流程，单点需求用更轻量的 skill 更合适
- 你希望 AI 完全自由发挥、不接受任何自查与硬门时 → 它的规则审计与 hooks 会介入（可关，但那就别装它）
- 你的场景不在上面命令表覆盖范围内时 → 先看命令表，没有对应命令就别硬套

## 目录结构

```
lhg-logo/
├── smoke_test.py          # 一键冒烟测试
├── ATTRIBUTION.md         # 灵感来源与许可声明
├── LICENSE                # MIT
├── README.md              # 本文件
├── .claude-plugin/
├── agents/
├── commands/
├── fixtures/
├── hooks/
├── scripts/
├── skills/
```

## 自检与反馈

本插件自带质检：每次使用后可跑 `python3 smoke_test.py` 一键验证（本次实测 51 项全部通过）。

发现 bug 或有改进建议，以 `[QC] <一句话问题>` 为标题提交到 https://github.com/lhg-plugs/lhg-logo/issues，正文写清"复现步骤 → 实际表现 → 期望表现"。

同门插件见 [lhg-plugs](https://github.com/lhg-plugs)，86 个插件的完整矩阵在 [marketplace](https://github.com/lhg-plugs/marketplace) 维护。

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 抖音：搜「刘老师讲AI实战」
- 微信：lhgsmsw
