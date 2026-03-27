# 文档黄金准则 (Documentation Golden Rules)

> 本文件包含文档同步层面的可检查准则。功能完成后必须逐条检查。

---

## 功能映射

- [GR-D001] **新增功能必须更新 feature-map.md**
  → 检查方法: `docs/feature-map.md` 中是否包含新功能的映射条目
  → 违规信号: 新增了用户可感知的功能，但 feature-map 无对应条目
  → 修复方式: 添加 `功能名 → 代码入口文件路径` 的映射
  → 来源: Done 定义

- [GR-D002] **删除功能必须清理 feature-map.md**
  → 检查方法: feature-map 中不应存在已删除功能的条目
  → 违规信号: 功能已移除但 feature-map 中仍有残留记录
  → 修复方式: 删除对应条目，检查是否有其他文档引用了该功能
  → 来源: 文档工程规则

---

## 变更日志

- [GR-D003] **用户可感知变更必须追加 CHANGELOG**
  → 检查方法: `CHANGELOG.md` 最新条目是否反映了本次变更
  → 违规信号: 新增了功能/修复了 bug 但 CHANGELOG 未更新
  → 修复方式: 按 Keep a Changelog 格式追加记录
  → 来源: 文档工程规则

---

## 架构文档

- [GR-D004] **模块结构变更必须更新 architecture.md**
  → 检查方法: `docs/architecture.md` 中的 Mermaid 图与实际代码结构一致
  → 违规信号: 新增了插件或修改了模块间关系，但架构图未更新
  → 修复方式: 更新对应的 Mermaid 代码块
  → 来源: 文档工程规则

- [GR-D005] **AGENTS.md 与项目结构一致**
  → 检查方法: 根目录 AGENTS.md 中的项目结构说明与实际目录一致
  → 违规信号: 新增了重要目录/文件但 AGENTS.md 未更新
  → 修复方式: 更新 AGENTS.md 的项目结构部分
  → 来源: Harness Engineering

---

## DSP 图谱

- [GR-D006] **模块变更必须同步 DSP 图谱**
  → 检查方法: `.dsp/graph.json` 与 `src/` 的模块结构一致
  → 违规信号: 新增/删除了模块但 graph.json 未同步
  → 修复方式: 更新 graph.json（参见 GR-A008、GR-A009）
  → 来源: DSP 架构协议

---

## 内联注释

- [GR-D007] **注释解释 Why 不解释 What**
  → 检查方法: 注释内容应解释"为什么这样做"而非"做了什么"
  → 违规信号: `// 设置变量 x 为 5`、`// 循环处理数组`
  → 修复方式: 删除显而易见的注释，在复杂逻辑处添加业务上下文注释
  → 来源: 文档工程规则

---

## ADR 决策记录

- [GR-D008] **核心技术决策必须创建 ADR**
  → 检查方法: `docs/adr/` 中是否记录了新依赖引入、API 变更、架构演化等决策
  → 违规信号: 引入了新的第三方库但无 ADR 文件
  → 修复方式: 在 `docs/adr/` 创建 ADR（格式参考已有 ADR）
  → 来源: 全局规则 / 决策沉淀

- [GR-D009] **已采纳 ADR 禁止直接修改**
  → 检查方法: 状态为"已采纳"的 ADR 不应有未标注的修改
  → 违规信号: 直接修改了已生效 ADR 的内容
  → 修复方式: 新建递增编号的 ADR，旧 ADR 标注 `状态: 已取代 → 参见 ADR-XXXX`
  → 来源: 全局规则 / 文档版本保护

---

## Implementation Plan 沉淀

- [GR-D010] **Implementation Plan 必须沉淀到 PLANS.md**
  → 检查方法: (1) `PLANS.md` 中不得出现「参见对话 artifact」「brain/」等悬空引用（正则: `参见对话|artifact|brain/[a-f0-9-]{36}`）; (2) `docs/handoff.md` 的「实施计划摘要」章节存在且 Plan 持久化位置指向 `PLANS.md`
  → 违规信号: (1) `PLANS.md` 中存在指向对话 artifact 目录的路径引用; (2) `docs/handoff.md` 缺少「实施计划摘要」章节; (3) `PLANS.md`「当前活跃计划」与 `handoff.md` 的任务描述不对齐
  → 修复方式: 将 Plan 精华同步到 `PLANS.md` 对应章节，悬空引用替换为内联内容或标注「已归档 → _versions/」
  → 来源: Harness Engineering 知识沉淀原则 / `/handoff` 工作流 §1.2.1 / `sdd:plan` 技能

- [GR-D011] **Markdown 内链严禁携带 `./` 或 `/` 路径修饰符**
  → 检查方法: 项目内索引（如 `PLANS.md` 或交接文档）中指向其他工单文件的超链接，必须使用纯净相对路径结构，如 `[名称](docs/plans/X.md)`
  → 违规信号: 出现了 `[名称](./docs/plans/X.md)` 或带反斜杠的伪绝对路径
  → 修复方式: 删除路标修饰符。防范外部独立极客渲染器（如 Obsidian / Notion 等）在解析 `./` 语义时发生的二级相对寻址越界（如错位搜索成 `../../`）导致死链
  → 来源: Markdown 泛解析器与双链笔记系统防腐防偏移策略
