---
description: 已有 logo.svg → 生成多尺寸导出包（favicon/社交/APP/印刷/深浅底/单色）+ 命名规范 + CHECKLIST。
argument-hint: [logo.svg路径] [--out delivery]
---

# /lhg-logo:logo-kit —— Logo 导出套件

用户输入在 `$ARGUMENTS` 中：`[logo.svg 路径] [--out 输出目录]`。输出缺省 `delivery/`。

加载 `lhg-logo-export`（第 3–4 节）。适用于：logo 已定稿，只差导出交付。

## 流程

### 1. 确认输入
- `logo.svg` 存在且过 `logo-audit`（blocker 清零）。没过审计 → 先修，不许带着病导出。
- 确认 `brand.json` 的 exports 清单（7 类场景）。

### 2. 生成导出包
- 按 lhg-logo-export 第 3 节清单生成各尺寸/格式；命名 `logo-<场景>-<尺寸>.<格式>`。
- 深底版、单色版单独导出，不许拿主版本将就。
- SVG 转 PNG 用矢量渲染（保持边缘清晰），favicon 16px 用简化版（如果主版本糊了）。

### 3. 对比度复算
- `logo_audit.py` 自动按 `contrast_pairs` 计算对比度；<4.5 的 warning 必须处理（加深标志色或换背景）。

### 4. 交付
- 输出 `delivery/` + `CHECKLIST.md`（走查打勾记录）。跑一遍 `logo-audit` 确认干净。

## 硬规则
- 印刷场景给 PNG → 不许，必须给矢量。
- 跳过审计直接打包 → 不许。
