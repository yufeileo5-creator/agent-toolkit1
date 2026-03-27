# AGENTS.md — AI Agent 上下文导航

> 本文件是 AI Agent 在本项目中工作的**首要入口**。Agent 进入项目后应首先阅读本文件，获取项目全貌和关键约束。

## 1. 项目概述

AI_UI 是一个基于**微内核 + 纯插件化架构**的 AI 可视化内容创作与应用管理平台。用户通过自然语言描述 UI 需求，AI 生成结构化布局数据，渲染到 Fabric.js 画布上，支持交互式编辑、导出和持久化。

## 2. 开发环境

```bash
# 依赖安装（严格使用 npm，禁止 pnpm / yarn）
npm install

# 启动开发服务器（前端 Vite :5173 + BFF Express :3001）
npm run dev:all

# 仅启动前端
npm run dev

# 仅启动 BFF
npm run server
```

- **Node.js**: ≥ 18
- **包管理器**: npm（锁文件 `package-lock.json`）
- **环境变量**: 复制 `.env.example` → `.env`，填入 API Key

## 3. 测试协议

```bash
# 运行全部测试
npx vitest run

# 监听模式
npx vitest

# 单文件测试
npx vitest run src/plugins/canvas-engine/canvas-commands.test.ts
```

- **框架**: Vitest
- **覆盖**: 核心模块（command-bus、hook-registry、canvas-commands）
- **约定**: 新功能必须先写测试（TDD），测试文件与源文件同目录

## 4. 代码风格

- **语言**: TypeScript（严格模式）
- **禁用 `any`**: 所有类型必须显式声明
- **函数长度**: 核心逻辑 ≤ 40 行，常规文件 ≤ 300 行
- **命名**: camelCase（变量/函数）、PascalCase（类型/接口/组件）
- **导入顺序**: 外部库 → 核心模块 → 插件模块 → 相对路径
- **注释语言**: 中文 Docstring，解释"为什么"而非"做什么"

## 5. PR 指南

- **提交格式**: Conventional Commits（`feat:`, `fix:`, `refactor:`, `docs:`, `test:`）
- **严禁直推 `main`**: 必须通过 PR
- **PR 描述**: 使用仓库模板，包含变更说明、影响范围、测试结果
- **触发 `pr-creator` 技能**: 创建 PR 时自动遵循

## 6. 项目结构与关键入口

```
C:\AgentCode\框架\
├── src/
│   ├── core/                    # 微内核（零业务逻辑）
│   │   ├── types.ts             # 全局接口契约
│   │   ├── plugin-manager.ts    # 插件加载引擎
│   │   ├── plugin-registry.ts   # 插件注册与类型路由
│   │   ├── hook-registry.ts     # 基于 tapable 的钩子中心
│   │   ├── command-bus.ts       # 命令总线（含 undo/redo）
│   │   ├── slot-manager.ts      # UI 插槽隔离渲染
│   │   └── health-monitor.ts    # 运行时健康监测
│   ├── plugins/                 # 所有业务能力
│   │   ├── canvas-engine/       # 画布引擎（→ 有子模块 AGENTS.md）
│   │   ├── ai-generate/         # AI 生成管线（→ 有子模块 AGENTS.md）
│   │   ├── property-panel/      # 属性编辑面板
│   │   ├── export-manager/      # 导出（PNG/SVG/React）
│   │   ├── project-persistence/ # 项目保存/加载
│   │   ├── layer-panel/         # 图层管理
│   │   ├── icon-picker/         # 图标选择器
│   │   └── plugin-marketplace/  # 应用市场
│   └── App.tsx                  # Shell 入口（五区布局）
├── server/                      # BFF 层（Express :3001）
│   └── routes/ai.ts             # AI API 路由
├── docs/
│   ├── architecture.md          # 系统架构概览
│   ├── feature-map.md           # 功能 → 代码映射
│   ├── adr/                     # 架构决策记录
│   ├── handoff.md               # 上下文交接文档
│   └── _versions/               # 历史版本归档
├── .dsp/graph.json              # DSP 依赖图谱（架构真相源）
├── .golden-rules/               # 黄金准则（可执行检查标准）
├── PLANS.md                     # 持久化设计文档
└── CHANGELOG.md                 # 变更日志
```

## 7. 分层约束（铁律）

```
Types → Config → Core → Plugin → UI
           ↓ 依赖方向（严禁反向）↓
```

| 层级 | 允许依赖 | 严禁依赖 |
|------|---------|---------|
| `types.ts` | 无外部依赖 | — |
| `core/*` | `types.ts` | 任何 `plugins/*` |
| `plugins/*` | `core/*`、`types.ts` | 其他 `plugins/*`（插件间零 import） |
| `App.tsx` | `core/*` | 直接 import `plugins/*` 内部模块 |

- **插件间通信**: 只能通过 `CommandBus`（命令）或 `HookRegistry`（钩子）
- **DSP 图谱**: `.dsp/graph.json` 是分层依赖的机器可读真相源
- **黄金准则**: `.golden-rules/architecture.golden.md` 包含可检查的具体规则
- **离线知识外脑 (Local RAG)**: 当调用复杂框架（如特定版本的 Fabric.js、第三方 C++ 侧图形库等）且记忆模糊时，绝对禁止凭空猜测或幻觉捏造 API。必须强制使用文件搜索工具优先检索 `docs/knowledge/` 目录下的官方快照。如果在里面查不到，立即挂起并请求人类喂送文档快照后方可下笔。

## 8. Done 定义

一个功能/修复被视为"完成"需要满足：

- [ ] 代码通过 TypeScript 编译（`tsc --noEmit`）
- [ ] 所有相关测试通过（`npx vitest run`）
- [ ] 不引入新的 lint 错误
- [ ] 架构分层未被破坏（无反向依赖）
- [ ] `docs/feature-map.md` 已更新（如涉及新功能）
- [ ] `CHANGELOG.md` 已追加（如涉及用户可感知变更）
- [ ] `.dsp/graph.json` 已同步（如涉及模块新增/删除/依赖变更）
- [ ] DSP 黄金准则检查通过
- [ ] **流水线排异 (CI/CD Verification)**: 若有远端门禁，提 PR 前必须查阅线上的 GitHub Actions/GitLab CI 报错日志确认绿灯（不只满足于本地 `npm run run test` 通过）。
- [ ] **视觉盲区验收 (Visual Handoff)**: 针对界面或样式（CSS/UI Component）的改动，测试通过不代表完成。Agent 必须主动暂停任务，要求人类开发者进行走查（Visual Regression），得到人类明确的验收许可后方可将该切片任务记为已完成。

## 9. 安全注意事项

- **API Key**: 严禁硬编码，必须通过 `.env` 注入，`.env` 已在 `.gitignore` 中
- **CORS**: BFF 层通过 `BFF_CORS_ORIGIN` 环境变量控制
- **速率限制**: AI 接口有 `express-rate-limit`（20次/15分钟）
- **文件操作边界**: Agent 只能修改项目目录内的文件

## 10. 规划文档指引（双层计划追踪）

- **完整方案 (Root)**: 复杂功能设计必须沉淀在 `docs/plans/` 的独立切片文件中（如 `FEAT-xxx.md`），并在 `PLANS.md` 中注册索引，避免单体文件膨胀及重度 Merge Conflicts。
- **阶段执行简报 (Artifact)**: 当前对话的临时实施计划对应 artifact 中的 `implementation_plan.md`。为避免跨交接后成为信息孤岛，其内部大标题必须命名为 `# Execution Brief — [当前子阶段]`，且**必须**在顶部提供返回 `PLANS.md` 对应章节的 Markdown 链接（例如 `> 📋 完整方案: [PLANS.md > 章名](file:///.../PLANS.md#...)`）。
- **隔离域与原子拆解 (Scoped Context & Micro-Tasking)**: 严禁写出粗粒度的大型任务包。任何一个 Checkbox 必须拆解尽到【单一组件级别】（不超过 3 个文件修改）。执行该原子任务时，AI 必须戴上“认知遮罩”，绝对禁止盲目扫描读取与之无关的同级模块代码，保持上下文极其纯净，模拟 Sub-Agent 的零干扰性。
- **重建机制 (Session Hydration) [🌟解决 Plan 存在感不高/找不到的问题]**: 由于 Artifacts（如 \`implementation_plan.md\`）不跨对话共享，**任何 AI 在 Handoff 后进入新对话，若检测到活跃计划切片，第一步必须主动**向上拉取该切片任务，在侧边栏重新写入 `implementation_plan.md`，以此恢复计划的存在感。
- **收尾反写 (Write-back)**: 在功能交付或准备执行 `/handoff` 前，Agent **必须**将当前 `implementation_plan.md` 中的完成状态（`[x]`）与执行结论，全量同步反写回具体分支计划文件（`docs/plans/`）中的执行跟踪面板，保持双向数据一致。
- **异脑交接 (Cross-Agent ADR Handoff)**: 接手涉及其他模块的新 Feature 时，不仅要读计划，**第一步必须强制加载查阅**该模块遗留的 `docs/adr/` 决策记录或相关 Handoff 简报，实现 AI 到 AI 的契约交接。
- **架构决策**: 在 `docs/adr/` 创建 ADR 文件
- **失败教训**: 沉淀到 `.golden-rules/` 或更新本文件

## 11. 渐进式规则路由（Progressive Disclosure）

> 技能按三层管理（Tier 1 常驻 / Tier 2 按需 / Tier 3 归档），避免注意力稀释。

### 技能分层

| 层级 | 路径 | 数量 | 加载时机 |
|------|------|------|---------|
| **Tier 1** | `C:\Users\Leo\.gemini\antigravity\skills\` | 7 | 每轮系统自动加载 |
| **Tier 2** | `C:\Users\Leo\.gemini\antigravity\skills\_on-demand\` | 16 | 特定任务时按需主动读取 |
| **Tier 3** | `C:\Users\Leo\.gemini\antigravity\skills\_archived\` | 11 | 需要时手动恢复 |

### 任务类型 → 核心规则映射

| 任务类型 | 必须优先加载的规则章节 | 按需加载的技能 |
|---------|---------------------|--------------|
| 🆕 新功能开发 | §2 架构守护 + §3 TDD | `sdd:plan`, `plugin-dev`, `feasibility-check`, `minimax-fullstack-dev`² |
| 🐛 Bug 修复 | §6 调试 + §7 验证 | `systematic-debugging`, `verification-before-completion` |
| 🔧 重构 | §2 + §3 + §7 | `regression-guard`, `code-review`² |
| 🎨 前端 UI | §4 前端标准 | `baseline-ui`², `taste-skill`², `interaction-completeness`², `minimax-frontend-dev`² |
| 📝 文档更新 | §8 文档工程 | `docs-writer`², `docs-changelog`² |
| 🧹 维护巡检 | §7 + §8 | `harness-gc`³, `dead-code-sweeper`³, `agent-eval`³ |
| 🔄 上下文交接 | §9 窗口守护 | `/handoff` 工作流 |

> 上标：无标 = Tier 1（自动加载），² = Tier 2（需从 `_on-demand/` 读取），³ = Tier 3（需从 `_archived/` 恢复）

### 始终生效规则（不可跳过）

无论任务类型如何，以下 5 条铁律始终生效：

1. **强制中文** — 所有输出使用中文（§1）
2. **禁止占位符** — 代码必须完整可运行（§1）
3. **AGENTS.md 优先** — 进入项目先读本文件
4. **分层约束** — 严禁反向依赖（§2 + 本文件 §7）
5. **验证后交付** — 证据优先于断言（§7）

### 黄金准则路由

| 准则文件 | 适用场景 |
|---------|---------|
| `architecture.golden.md` | 修改 `src/` 下的 import、新增模块 |
| `code-quality.golden.md` | 每次代码修改 |
| `documentation.golden.md` | 功能完成后（配合 `/doc-sync-check`）|
| `sandbox-security.golden.md` | 涉及文件操作、API 调用、环境变量 |
| `error-hints.golden.md` | 遇到已知错误模式时 |

> **迭代改进原则**: Agent 犯同样错误 2 次 → 检查是否需要更新本 AGENTS.md 或 `.golden-rules/`
> **缓存机制 (I/O 优化)**: 同一轮上下文中，对应场景的 `.golden-rules` 首次触发时读取一次即可，后续同一场景的多次修改严禁重复调用 `view_file` 检索，请充分利用短期记忆。
