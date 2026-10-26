<!-- About 简介（推送后填写到仓库 About 栏）：
Logo设计专家：品牌简介→多版概念→几何规范→多尺寸导出→应用自检 ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-logo
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, logo, branding, svg -->

# lhg-logo：Logo设计专家

> **一句话介绍**：品牌简介→设计简报→3 版概念→几何规范→SVG 源文件→多尺寸导出清单→应用场景自检，端到端交付 logo 资产包；16 条确定性规则全程护航。
>
> **一键安装**：在 Claude Code 里运行
> ```
> /plugin marketplace add lhg-plugs/lhg-logo
> /plugin install lhg-logo@lhg-plugs
> ```

## 它是什么

`lhg-logo` 是一个 Claude Code 插件（plugin 为主、skill 为辅），专为"想要一个 logo 但不知道从哪下手"的小商家与个人品牌设计：

- **4 个命令**（小白入口）：`logo` 一句话出 logo 资产包（简报→概念→规范→导出→自检），`logo-audit` 确定性审计，`logo-kit` 已有 SVG 一键出多尺寸导出包，`logo-critique` 概念评审（原创性+商标风险提示）
- **4 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等 agent 平台）：品牌简报、概念发想、几何规范、导出与应用自检
- **3 个专家 agent**：品牌设计师、规范审计师、原创性评审员（设计与评审隔离）
- **1 个硬门 hook**：导出/交付前自动校验 SVG 规范（viewBox/空元素/解析失败拦截，可一键豁免，不骚扰）
- **16 条确定性自查规则**：SVG 规范 6、尺寸覆盖 3、色彩对比度 2、版本 3、合规 2，纯 Python、零第三方依赖，秒级出结果

工作流：`logo`（端到端）或分段用：简报→`logo-critique`（评审概念）→规范→`logo-kit`（导出）→`logo-audit`（查一遍）。

## 4 个命令用法

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-logo:logo` | 品牌简介→简报→3 版概念→几何规范→SVG→导出→自检 | `/lhg-logo:logo "社区咖啡店，主打手冲" --scene social` |
| `/lhg-logo:logo-audit` | SVG/尺寸/色彩/版本 16 条规则审计 | `/lhg-logo:logo-audit ./delivery/` |
| `/lhg-logo:logo-kit` | 已有 logo.svg→多尺寸导出包+命名规范 | `/lhg-logo:logo-kit ./logo.svg --out ./delivery/` |
| `/lhg-logo:logo-critique` | 概念评审：原创性+商标风险提示+三项生存测试 | `/lhg-logo:logo-critique ./concepts.md` |

## 自查说明

自查 = 确定性脚本（机器）+ 人工评审清单（人）：

1. 先跑 `scripts/audit/logo_audit.py`（16 条规则），零 LLM 成本；
2. 发现分三级：**blocker**（必须修，导出前 hook 会拦截坏 SVG）、**warning**（修或书面记录已知问题）、**nit**（顺手修）；
3. 再按 `lhg-logo-export` 第 5 节做应用场景走查（16px 肉眼/圆切/深色/单色/远距离/竞品并排）。

blocker 清零才算做完；为清零改规则算作弊，不许。

## 目录结构

```
lhg-logo/
├── .claude-plugin/          # plugin.json（插件清单）+ marketplace.json（本仓即市场）
├── commands/                # 4 个命令：logo / logo-audit / logo-kit / logo-critique
├── skills/                  # 4 个平台中立 skill（简报/概念/几何规范/导出自检）
├── agents/                  # 3 个专家 agent（designer / spec-auditor / originality-reviewer）
├── hooks/                   # 1 个硬门（导出前 SVG 校验）+ 豁免说明
├── scripts/audit/           # 16 条确定性自查规则（零第三方依赖）
├── fixtures/                # 冒烟测试用例（坏/好对照，均为虚构品牌）
├── smoke_test.py            # 一键冒烟测试
├── ATTRIBUTION.md           # 灵感来源与许可声明
└── LICENSE                  # MIT
```

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用：**

- 你开了个小店/做了个产品，想要个 logo 但请不起设计公司时 → 用 `/lhg-logo:logo`，一句话出资产包
- 你已经有个 logo（甚至只是 JPG），想把它变成规范资产时 → 走简报→几何规范重建，再用 `/lhg-logo:logo-kit` 导出
- logo 做好了，怕到处用时翻车（favicon 糊了、深色底没法用、印刷放大糊）时 → 跑 `/lhg-logo:logo-audit`
- 拿不准 logo 会不会跟别人"撞脸"时 → 用 `/lhg-logo:logo-critique` 先评审

**什么时候不用：**

- 你要的是整套品牌视觉（VI 手册、包装、门店空间）→ 本插件是"logo"专家，只做标识本身及其直接导出物
- 你需要有法律效力的商标检索结论 → 本插件只给风险提示，不构成商标检索与法律意见，正式商用前请咨询专业人士

**风险点诚实说明：**

- **不承诺商标结果**：评审只能基于简报避让清单+公开常识做原创性审查，不能替代专业商标近似检索；`logo-critique` 会把这段话写进交付物
- **AI 生成图形的边界**：本插件的方法论是"规范与流程"，不替你"画"出最终艺术品——概念阶段的视觉呈现需要设计师（人或 AI 绘画）执行，插件保证的是流程不跑偏、交付不缺件
- **色彩对比度是启发式**：按 WCAG 公式计算，覆盖常见场景；特殊材质（烫金/刺绣）请以打样为准
- **示例均为虚构**：插件内所有 logo 示例（fixtures/svg）均为虚构品牌，未使用任何真实品牌标识

## lhg-plugs 插件矩阵

| 插件 | 一句话 | 安装 |
|---|---|---|
| [lhg-logo](https://github.com/lhg-plugs/lhg-logo) | 品牌简介→多版概念→几何规范→多尺寸导出→应用自检 | `/plugin install lhg-logo@lhg-plugs` |
| [lhg-headline](https://github.com/lhg-plugs/lhg-headline) | 主题/内容→多平台标题公式生成→敏感词检测→点击率打分 | `/plugin install lhg-headline@lhg-plugs` |
| [lhg-video-edit](https://github.com/lhg-plugs/lhg-video-edit) | 一句话把口播素材剪成爆款短视频（+口播脚本子命令） | `/plugin install lhg-video-edit@lhg-plugs` |
| [lhg-fullstack](https://github.com/lhg-plugs/lhg-fullstack) | 小白一句话 → 高质量全栈应用 | `/plugin install lhg-fullstack@lhg-plugs` |

## 自检与反馈

本插件自带质检：每次使用后可跑 `python3 smoke_test.py` 一键验证（JSON 合法、skill/command/agent 完整性、16 条规则、fixtures 命中、hooks 行为）。

发现 bug 或有改进建议，以 `[QC] <一句话问题>` 为标题提交到 https://github.com/lhg-plugs/lhg-logo/issues，正文写清"复现步骤 → 实际表现 → 期望表现"。

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 抖音：搜「刘老师讲AI实战」
- 微信：lhgsmsw
