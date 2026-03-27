# PLANS.md — 持久化设计文档

> 本文件是 Implementation Plan 的**项目级持久化归宿**，跨对话/跨 Agent 可见。
>
> **生命周期**: 对话 artifact 中的 `implementation_plan.md` 是草稿区 → 用户批准后进入 EXECUTION →
> **收尾反写 (Write-back)**: 在功能交付或准备执行 `/handoff` 前，Agent **必须**将当前 `implementation_plan.md` 中的完成状态（`[x]`）与执行结论，全量同步反写回具体切片文件中的[执行跟踪]面板，保持双向数据一致。
>
> **交接 (Handoff)**: Handoff 时 Agent 记录当前快照（参见 `/handoff` 工作流）→ 新 AI 进场。
>
> **重建机制 (Session Hydration)**: 新 AI 启动后如果检测到存在[当前活跃计划]，**必须直接以该切片计划为准，在当前的 Artifact 侧边栏重新生成一份 `implementation_plan.md`**，以此解决跨对话后 Artifact 丢失、存在感低的问题！
>
> **黄金准则**: GR-D010 要求每次 Handoff 后 PLANS.md 必须与 implementation_plan 保持同步。严禁出现「参见对话 artifact xxx」的悬空引用。

---

## 📂 活跃计划切片 (Active Slices)

*为了防膨胀与并发冲突，当前项目实行【切片化管理】。此处仅作总索引，具体内容请点击穿透至子工单。*

- 🟣 [FEAT-long-form: 长图文生成主线 (P2强化阶段)](docs/plans/FEAT-long-form.md) `Status: Doing`

## 🗄️ 归档库 (Archived Slices)

*已完成的独立或大型重构项目索引。*

- 🟢 [ARCH-harness-engineering: 挂载工程化极简集](docs/plans/FEAT-mock-example.md) `Status: Done` (历史记录摘要已提取至 README / AGENTS)
- 🟢 [REFACTOR-design-system-cascade: 设计系统级联重构] `Status: Done`
- 🟢 [ARCH-microkernel-plugin: 微内核+插件化架构一期] `Status: Done`
