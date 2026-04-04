# Antigravity Agent Toolkit (Harness Config Repository)

> 🕒 **Last Synchronized:** 2026-04-04
> 🤖 **Maintained By:** Antigravity AI Agent

This repository contains the global configurations, skills, and workflows for the Antigravity Agent ecosystem. It serves as a centralized "Harness" that can be quickly cloned and deployed to any new machine or environment.

## 🛠️ Auto-Installers Deployment

You can instantly bootstrap your Antigravity environment by running one of the provided scripts.
This will copy all the rules, skills, and templates to your local `~/.gemini/antigravity/` directory.

- **Windows:** Right-click `install.ps1` and run with PowerShell, or run `.\install.ps1` in the terminal.
- **Mac/Linux:** Run `bash install.sh` or `./install.sh` in the terminal.

## 🧠 Core Design Rules & Architecture

This toolkit heavily relies on the global system rules (`GEMINI.md`) and a layered defense logic:
1. **Requirements Completion Protocol (需求补全):** AI acts as a Requirements Officer, asking clarifying questions before executing any ambiguous instructions.
2. **Feasibility Checks & SDD:** Complex features enforce a feasibility check and Software Design Document (`implementation_plan.md`) approval before coding.
3. **P.U.A Engine:** Prevents the AI from giving up prematurely.
4. **Data Structure Protocol (DSP) & Architecture:** Forces AI to check `.dsp/graph.json` or architectural diagrams and keep module boundaries clean.

## 🧰 Skill Catalog (技能矩阵)

Skills are separated into three tiers to prevent LLM attention dilution.

### Tier 1 (Core Skills) - Always Loaded
| Skill Name | 功能描述 |
| --- | --- |
| `feasibility-check` | **可行性审查**：强制审查新功能的技术与架构可行性，拒绝执行不可行需求并提供替代方案。 |
| `plugin-dev` | **插件开发**：AI 编写新功能插件的标准指南，包含生命周期和注册规范。 |
| `pua` | **反摆烂引擎**：当 AI 尝试放弃、盲目重试或让用户自己操作时，强制触发穷尽方案逻辑。 |
| `regression-guard` | **回归守卫**：修改现有代码时强制触发的功能防破坏系统（含 Diff 推导与测试）。 |
| `sdd-plan` | **规格驱动开发**：强制要求在编码前进行详细的任务切片设计和审批。 |
| `systematic-debugging` | **系统化调试**：解决 Bug 时的四段式诊断法则，禁止盲目依靠直觉打补丁。 |
| `verification-before-completion` | **验证后交付**：AI 宣称任务完成前，必须附带自动化测试或命令行运行通过的日志证据。 |

### Tier 2 (On-Demand Skills) - Loaded when needed
| Skill Name | 功能描述 |
| --- | --- |
| `baseline-ui` | 提供 UI 基础组件库和极简设计语言的审美基线指导。 |
| `code-review` | 自动审查代码质量、架构合规度与可维护性。 |
| `data-structure-protocol` | 针对特定数据结构的存储、读取和修改的标准化契约系统。 |
| `docs-changelog` | 梳理和生成项目的自动变更更新日志（CHANGELOG）。 |
| `docs-writer` | 自动生成、维护及校验研发文档和 API 技术手册。 |
| `feature-tracer` | 分析及追踪特定功能模块从入口到内核的全链路实现。 |
| `interaction-completeness` | 前端交互五态（加载、空、成功、报错、禁用）的完整性审查。 |
| `log-compressor` | 终端日志压缩清洗工具，应对过长报错日志，提取 Root Cause。 |
| `long-form-content` | 长文本和文章类型内容的深度生成排版。 |
| `minimax-frontend-dev` / `minimax-fullstack-dev` | 前端或全栈开发专项极速编码规约指引。 |
| `minimax-multimodal-toolkit` | 多模态输入转 UI 和功能的专用套件。 |
| `performance-auditor` | 前端渲染与后端接口的性能诊断审核专家。 |
| `pr-creator` | Pull Request 生成助手，含标准模板和 Diff 摘要。 |
| `react-best-practices` | 基于 Hooks 的 React 现代写法守护。 |
| `skill-creator` | Agent 自我延展，用于帮用户编写最新的技能卡片。 |
| `taste-skill` | 负责微动画和玻璃拟物化等高级交互设计评估。 |
| `test-driven-development` | TDD 红绿循环测试驱动开发强制准则。 |
| `webapp-testing` | 端到端 Web UI 验收测试。 |

### Tier 3 (Archived Skills) - Restored Manually
| Skill Name | 功能描述 |
| --- | --- |
| `agent-eval` | Agent 能力自评与表现回顾组件。 |
| `canvas-design` | Canvas 编辑器和拖拽业务的绘图架构设计。 |
| `dead-code-sweeper` | 僵尸代码自动扫描及清理卫士。 |
| `harness-gc` | 针对项目的全局依赖垃圾回收和状态重置。 |
| `mcp-builder` | 辅助构建 MCP (Model Context Protocol) 扩展服务器。 |
| `pm-xxx` | 虚拟产品经理场景下的语法增强/虚拟数据集生成/SQL构建等组件。 |
| `pdf` / `playwright-skill` | 独立领域的分析测试技能。 |

## 🔄 Workflows Guide (工作流指南)

| Workflow Command | Description | Trigger Scenario |
| --- | --- | --- |
| `/handoff` | **上下文交接工作流**。生成包含全链路进度、重大架构决策和未决问题的交接文档。 | 当会话过长大模型性能下降，或里程碑完成需开启新窗口时。 |
| `/plan` | **计划模式工作流**。强制开启 `implementation_plan.md` 的构建设计阶段。 | 接受到大型、发散度高、涉及多个核心功能时。 |
| `/doc-sync-check` | **文档同步检查**。检查 Feature-map、Graph 和 Changelog 是否更新。 | 一段重要的功能交付和验收完成后。 |
| `/layout-engine-check` | **排版引擎检查清单**。专门针对渲染引擎层的功能防线。 | UI 核心或图层管理逻辑发生变动时。 |
| `/version` | **版本管理工作流**。快速打包、提交、打标签推送代码。 | 确认功能稳定上线或交付前。 |
| `/sync-harness` | **全局配置互斥同步同步工作流**。将本地的 Prompt、Skills 和 Templates 更新到这个中央仓库。 | 技能群或工作流发生重大改进时。 |
