---
description: Logo 确定性审计：SVG 规范（viewBox/文字转曲/空元素）+ 尺寸覆盖 + 色彩对比度 + 深浅底/单色版本，16 条规则。
argument-hint: [delivery目录]
---

# /lhg-logo:logo-audit —— Logo 确定性审计

用户输入在 `$ARGUMENTS` 中：`[delivery 目录]`。缺省扫描当前目录。

## 流程

### 1. 跑脚本
```bash
python3 scripts/audit/logo_audit.py --target <目标> --format text
```
16 条规则（SVG 6、尺寸 3、色彩 2、版本 3、合规 2），零第三方依赖。exit code 语义：2=有 blocker，1=有 warning，0=干净。

### 2. 分级处理
- **blocker**（无 viewBox/SVG 解析失败/空元素/brand.json 非法）：必须修。
- **warning**（文字未转曲/缺 favicon/对比度不足/无深色版/无单色版）：修，或书面记录已知问题。
- **nit**（缺 `<title>`/色数多/安全区未声明/无原创性声明）：顺手修。

### 3. 人工走查（脚本查不到的）
- 16px favicon 肉眼：认得出吗？
- 竞品并排：第一眼分得清吗？
- 深底版是单独调过的吗？（不是反色将就的）

### 4. 交付
- blocker 清零才算过；输出审计报告 + CHECKLIST.md 打勾记录。

## 硬规则
- blocker 未清零交付 → 不许（导出前 hook 会拦截坏 SVG）。
- 为过检改规则 → 作弊，不许。
