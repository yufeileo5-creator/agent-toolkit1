---
description: >-
  文档同步检查工作流。功能完成后触发，逐项确认 feature-map、architecture、CHANGELOG、DSP graph.json、AGENTS.md 是否已同步更新。比 harness-gc 更轻量，适合单次功能交付后的快速检查。
---

# 📋 文档同步检查工作流 (Doc Sync Check)

**触发条件**: 功能开发完成标记 `[x]` 后、代码审查前、交付验证阶段

> [!IMPORTANT]
> 本工作流是 `.golden-rules/documentation.golden.md` 的快速执行版，不替代完整的 `harness-gc` 巡检。

---

## 检查清单

按以下顺序逐项检查，每项标注 ✅ 通过 / ❌ 未通过 / ⏭️ 不适用：

### 1. feature-map.md (GR-D001 / GR-D002)
- 本次变更是否涉及新增或修改用户可感知的功能？
  - 是 → 检查 `docs/feature-map.md` 是否已添加/更新对应条目
  - 否 → ⏭️ 跳过

### 2. CHANGELOG.md (GR-D003)
- 本次变更是否属于用户可感知的功能变更、Bug 修复或破坏性变更？
  - 是 → 检查 `CHANGELOG.md` 是否已追加条目（Keep a Changelog 格式）
  - 否 → ⏭️ 跳过

### 3. architecture.md (GR-D004)
- 本次变更是否涉及新增/删除模块、修改模块间依赖关系？
  - 是 → 检查 `docs/architecture.md` 中的 Mermaid 图是否已更新
  - 否 → ⏭️ 跳过

### 4. AGENTS.md (GR-D005)
- 本次变更是否涉及新增重要目录/文件、修改项目结构？
  - 是 → 检查根目录 `AGENTS.md` 的项目结构部分是否已更新
  - 否 → ⏭️ 跳过
- 本次变更是否修改了特定子模块（canvas-engine / ai-generate）的内部结构？
  - 是 → 检查对应的子模块 `AGENTS.md` 是否已更新
  - 否 → ⏭️ 跳过

### 5. DSP graph.json (GR-D006 / GR-A008 / GR-A009)
- 本次变更是否涉及新增/删除模块、修改模块依赖？
  - 是 → 检查 `.dsp/graph.json` 是否已同步更新
  - 否 → ⏭️ 跳过

### 6. ADR (GR-D008)
- 本次变更是否涉及核心技术决策（新依赖引入、API 变更、架构演化）？
  - 是 → 检查 `docs/adr/` 是否已创建对应的 ADR 文件
  - 否 → ⏭️ 跳过

### 7. PLANS.md
- 本次变更是否与 `PLANS.md` 中的某个活跃计划相关？
  - 是 → 检查计划状态是否已更新（完成的计划移至归档）
  - 否 → ⏭️ 跳过

---

## 输出格式

完成检查后，输出简洁报告：

```
📋 文档同步检查结果:
✅ feature-map.md — 已更新
✅ CHANGELOG.md — 已追加 v1.2.0 条目
⏭️ architecture.md — 不适用（无模块变更）
✅ AGENTS.md — 已更新项目结构
⏭️ DSP graph.json — 不适用
⏭️ ADR — 不适用
✅ PLANS.md — 计划状态已更新

全部通过 ✅ | 阻断项: 0
```

如有 ❌ 项，在报告后附修复步骤。

---

## 与 harness-gc 的关系

| 维度 | doc-sync-check | harness-gc |
|------|---------------|------------|
| 范围 | 仅文档同步 | 文档 + DSP + 死代码 + 代码质量 |
| 粒度 | 针对本次变更 | 全库扫描 |
| 速度 | 快（1-2 分钟） | 慢（5-10 分钟） |
| 适用 | 每次功能完成后 | 定期巡检 / 跨期交接前 |
