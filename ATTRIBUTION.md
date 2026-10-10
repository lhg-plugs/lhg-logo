# 灵感来源与致谢（Attribution）

本插件的**方法论灵感**来自以下优秀的开源项目，**所有实现代码、检测规则与文案均为原创**，未复制任何第三方的原文案、代码与 logo 语料。

| 项目 | 作者 / 组织 | 许可 | 链接 | 借鉴了什么思路 |
|---|---|---|---|---|
| logo-design-skill | kaankiziltug | MIT（skill 文本/脚本/模板部分；见下文商标声明） | https://github.com/kaankiziltug/logo-design-skill | "简报→多概念→几何规范→测试表→导出套件"的品牌设计流程思想；SVG 审计思路（viewBox 校验、文字转曲提醒）；深浅底/单色版本测试；"不承诺商标结果"的诚实声明。**实现与文案全部原创** |
| impeccable | pbakaus | Apache-2.0 | https://github.com/pbakaus/impeccable | 设计语言与品牌规范的方法论思路（规范先行、确定性校验）。**实现与文案全部原创** |

热度核实（2026-10-11 实查）：
- `kaankiziltug/logo-design-skill`：MIT 许可（`gh api` 实查 `license=MIT`，stars 约 2.6k）；其 README 明确声明 `assets/library/svg/` 下的 1400+ 真实品牌 logo **不受 MIT 许可覆盖**（见其 TRADEMARKS.md），仅作学习参考。
- `pbakaus/impeccable`：Apache-2.0 许可（`gh api` 实查，stars 约 79.3k）；调研报告（2026-10-10）中记为 62k，为当时数据。
- 调研报告（2026-10-10）将"品牌 Logo 设计"列为第 22~23 名区间（总分 14/20），结论为"小商家刚需；可整合设计 skill 的品牌规范部分"——本插件即按此立项。

## 商标与语料红线声明

1. **绝不复制真实 logo 语料库**：`kaankiziltug/logo-design-skill` 的 `assets/library/svg/` 真实品牌 logo 文件受其 TRADEMARKS.md 约束（商标归各自所有者，MIT 不覆盖），本插件**未下载、未复制、未参考其中任何文件**。
2. **本插件所有示例均为虚构**：`fixtures/` 下的 SVG 与 `brand.json`、skill 文中的品牌案例（如"示例品牌"）均为独立虚构，不指向任何真实品牌；如有雷同，纯属巧合。
3. **借鉴思路，实现与文案均为原创**：以上项目的具体文案、规则原文、代码实现均未被复制。本插件的 skill 方法论文案、审计规则、命令流程、hook 脚本均为独立撰写。
4. **许可合规**：上述项目分别为 MIT / Apache-2.0 许可，允许在保留声明的前提下进行思路借鉴与二次创作。本文件即为保留声明的一部分。
5. **商标与归属**：各项目名称与作者署名归其各自所有者所有。本插件不提供商标检索服务，不构成法律意见（见 `logo-critique` 命令）。

## 本插件自身的许可

本插件原创部分采用 MIT 许可（见 `LICENSE` 文件），版权所有：刘洪光（https://github.com/lhg-skills）。
