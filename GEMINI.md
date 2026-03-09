## 🤖 Antigravity 全局代理规则 (Global Agent Rules)

---

### 1. 语言与交互 (Language & Communication)

* **强制中文：** 所有对话、分析说明、错误解释、代码注释（Docstring）及生成的文档必须使用**中文**。
* **推理可见化：** 执行任何文件修改或终端命令**之前**，必须在回复中用中文简要解释：意图（为什么做）、风险（可能的破坏）、预期（结果）。
* **禁止占位符：** 严禁生成 `// ... existing code` 等残缺代码块。所有修改必须完整且可直接运行。
* **主动技能调度 [★新增]：** 遇到特定场景，你必须**主动**检查 `.agents/skills/` 目录，并严格按照对应的 Skill 指令执行，严禁自行发挥。
* **技能创建与优化 (skill-creator)：** 创建或优化 Agent Skill 时，必须触发 `skill-creator` 技能，遵循标准 SKILL.md 格式和描述优化最佳实践。

---

### 2. 需求拆解与架构守护 (Planning & Architecture)

* **规格驱动开发 (sdd:plan)：** 接到复杂需求时，禁止立刻写代码。必须先触发 `sdd:plan` 技能，完成研究、方案生成和 7 阶段质量审查，产出 `implementation_plan.md` 待用户批准。
* **图谱驱动 (data-structure-protocol)：** 在修改核心文件、添加或删除依赖前，禁止盲搜代码。
  1. 必须使用 `dsp-cli` 检索 `.dsp/` 目录获取当前的实体依赖关系。
  2. 凡涉及新建模块、修改导出或增删依赖，必须**强制同步写入 DSP 图谱**，维持架构记忆。
* **架构约束：** 严禁打破领域模型分层。禁止跨层循环依赖，新引入第三方库必须先向用户申请。
* **流程图强制 [★新增]：** 在 `implementation_plan.md` 中，必须使用 **Mermaid** 产出至少一张可视化图表（流程图 `flowchart`、时序图 `sequenceDiagram`、架构图 `C4Context` 等，视需求选择）。禁止纯文字描述复杂逻辑流转，图文必须并存。
* **MCP 开发规范 (mcp-builder)：** 构建 MCP Server 集成外部 API/服务时，必须触发 `mcp-builder` 技能，遵循四阶段工作流（研究规划 → 实现 → 审查测试 → 评估创建）。

---

### 3. 先发制人：测试驱动 (Test-Driven Development)

* **TDD 铁律：** 写业务代码前，必须先写出对应的测试（RED）。如果不先跑一次会报错的测试，绝对不允许写任何实现代码（GREEN）。
* **原子性保证：** 跨文件修改时，按"被依赖方先改"的依赖顺序编排，确保任何中间状态都可通过测试。
* **破坏性变更预警：** 删改导出 API、数据库字段、环境变量时，必须**显式标注** `⚠️ BREAKING CHANGE` 并等待确认。

---

### 4. 极致前端与工程标准 (High-Agency Frontend & Engineering)

* **反大厂AI味审美 (taste-skill)：** 严格执行现代极简设计。禁止系统自带默认 Glow/紫光、禁止默认丑大头条、必须使用高对比度/高品质排版（如 Geist/Satoshi）、强制物理反馈微动效（如需要动效）。
* **UI 基线 (baseline-ui)：** 动画不能超过 200ms、禁止用 `h-screen`（用 `h-dvh`）、严禁随意设 `z-index`。强制遵守结构可访问性设计。
* **React 性能 58 条法则 (react-best-practices)：** 遇到前端文件时，严禁引发瀑布流请求、强制正确使用 Server/Client Component、避免不必要的重渲染。
* **后端准则：** 严格类型安全（禁用 `any`），坚守单一职责（核心函数不超过 40 行，常规文件 300 行警戒），所有 I/O 数据强制防御性校验。
* **视觉设计创作 (canvas-design)：** 当用户要求创建海报、艺术品、视觉设计等静态作品时，必须触发 `canvas-design` 技能，遵循设计哲学驱动的两阶段创作流程（哲学定义 → 画布表达）。
* **交互完整性审查 (interaction-completeness)：** 实现任何面向用户的前端功能后，必须触发 `interaction-completeness` 技能，逐项检查五态（空/加载/错误/成功/禁用）、边界条件、键盘可达性、防抖节流、撤销恢复和响应式适配，确保"能用"且"好用"。

---

### 5. 环境感知 (Environment Awareness)

* **自动适配包管理器：** Node.js/TS 严格遵守锁文件（严禁混用 pnpm/npm/yarn），Python 强制使用 `uv`。
* **环境变量保护：** 严禁硬编码敏感信息。必须存入 `.env`，并行更 `.env.example`。

---

### 6. 系统化调试 (Systematic Debugging)

* **严禁盲目重试：** 遇到错误，必须立刻触发 `systematic-debugging` 技能执行完整的四阶段诊断。
* **查证溯源：** 必须阅读底层 Error Trace，在中文日志中给出真正的"Root Cause"，必须先构造复现环境和假设，严厉禁止"试试重新安装"。

---

### 7. 交付门槛禁区 (Verification & Code Review)

* **完成前强制验证 (verification-before-completion)：** 在说"已修复"、"已完成"前，必须运行具体的验证脚本/测试命令，并确认输出终端里没有出现新增的 Error 或 Warning，*必须让证据优先于断言*。
* **Web 应用测试 (webapp-testing)：** 验证前端功能或调试 UI 行为时，触发 `webapp-testing` 技能，通过 Playwright 编写自动化测试脚本进行端到端验证。
* **本地代码审查 (code-review)：** 重要的阶段完成前，触发六大虚拟特工（Bug 猎手/安全审计/代码质量/等）对未提交的变更进行联合巡察，评分并列出确切修复意见再交付结果给用户。
* **PR 创建规范 (pr-creator)：** 创建 Pull Request 时，必须触发 `pr-creator` 技能，确保 PR 遵循仓库模板标准、包含完整描述、使用 Conventional Commits 格式，且严禁直接推送到 `main` 分支。
* **决策沉淀 (ADR)：** 对于重大技术方案的定型、依赖的替留，应在 `docs/` 创建 ADR 记录，作为项目长期遗产。

---

### 8. 文档工程 (Documentation Engineering) [★新增]

* **README 强制：** 每个项目根目录必须存在 `README.md`，包含：项目简介、技术栈、快速启动指南、目录结构说明。新建项目时必须同步创建，已有项目在功能变更后必须同步更新。
* **API 文档：** 所有对外暴露的函数/接口必须编写 **TSDoc / JSDoc / Docstring**（视语言而定），包含参数说明、返回值、异常情况。禁止裸导出无注释的公共 API。
* **技术文档写作 (docs-writer)：** 编写、审查或编辑 `/docs` 目录或任何 `.md` 文件时，触发 `docs-writer` 技能，遵循四阶段流程（标准制定 → 准备调研 → 执行写作 → 验证定稿）。
* **变更日志 (docs-changelog)：** 每次有用户可感知的功能变更、Bug 修复或破坏性变更时，触发 `docs-changelog` 技能，在 `CHANGELOG.md` 中按 [Keep a Changelog](https://keepachangelog.com/) 格式追加记录。
* **PDF 文档处理 (pdf)：** 涉及 PDF 文件的任何操作（读取、合并、拆分、水印、表单填写、加密、OCR 等），必须触发 `pdf` 技能，使用推荐的 Python 库和命令行工具链。
* **架构文档：** 对于多模块/多服务项目，必须在 `docs/architecture.md` 中维护系统架构概览，包含 Mermaid 架构图和模块职责说明。架构发生变更时必须同步更新。
* **内联注释标准：** 注释用于解释 **为什么 (Why)**，而非 **做什么 (What)**。禁止无意义注释（如 `// 设置变量`），鼓励在复杂业务逻辑处添加上下文注释。
