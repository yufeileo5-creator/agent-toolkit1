# 🤖 Agent Toolkit v6.0 (T0 Architecture)

> AI Agent 的全局配置、技能和工作流集合。  
> 基于 **OpenAI Harness Engineering** 范式构建，让 AI 不靠自觉，靠体系。

---

## 🚀 极速安装 (Quick Start One-Liner)

无论你是在新电脑开荒，还是分享给新同事，只需在终端运行下方的 **一行命令**，即可全自动实现旧版备份，并从云端拉取整套神级战甲覆盖当前系统：

**👉 Windows (PowerShell):**
```powershell
iwr -useb https://raw.githubusercontent.com/yufeileo5-creator/agent-toolkit1/main/install.ps1 | iex
```

**👉 Mac / Linux (Bash):**
```bash
curl -fsSL https://raw.githubusercontent.com/yufeileo5-creator/agent-toolkit1/main/install.sh | bash
```
> 行星级同步：只要提示“安装完成”，重启 IDE 即代表你新电脑已接管最新的 93 个大厂私有技能与防爆破核心规则！

---

## 📋 这是什么？

这是一套 **AI 开发 Agent 的全局知识底座**，包含：

- 🧠 **全局规则** (`GEMINI.md`) — 10 个章节，约束 Agent 的所有行为
- ⚡ **93 个技能** — 从架构守护到产品管理，按需触发的专业能力
- 🔄 **5 个工作流** — 标准化的开发流程（计划/交接/版本/巡检）

安装到 `~/.gemini/` 后，Agent 在**所有项目**中自动加载这些规则和能力。

---

## 🏗️ 体系架构

```
基于 OpenAI Harness Engineering 七大核心组件：

┌─────────────────────────────────────────────────┐
│              Context Engineering                 │
│    GEMINI.md（全局规则）+ AGENTS.md（项目级）      │
├──────────────────┬──────────────────────────────┤
│  Architectural   │        Agent Loop            │
│  Constraints     │  sdd:plan → 实现 → verify    │
│  分层依赖 + DSP   │  pua → 失败沉淀 → 自修复      │
├──────────────────┼──────────────────────────────┤
│ Garbage          │  Evaluation                  │
│ Collection       │  Harness                     │
│ harness-gc 巡检  │  agent-eval 四维评估          │
├──────────────────┴──────────────────────────────┤
│  Tool Integration (MCP) + Sandbox Security       │
└─────────────────────────────────────────────────┘
```

---

## 📂 目录结构

```
~/.gemini/
├── GEMINI.md                           # 全局代理规则（v5，10 章节）
├── README.md                           # 本文件
├── _versions/                          # GEMINI.md 历史版本归档
│
└── antigravity/
    ├── templates/                      # 🏗️ T0 核心母版库 (含 AGENTS.md/PLANS.md)
    ├── skills/                         # ⚡ 93 个技能
    │   ├── harness-gc/                 #   代码库四维巡检
    │   ├── agent-eval/                 #   Agent 质量评估
    │   ├── pua/                        #   反摆烂引擎 + 失败沉淀闭环
    │   ├── sdd-plan/                   #   规格驱动开发
    │   ├── systematic-debugging/       #   系统化调试
    │   ├── code-review/                #   六特工代码审查
    │   ├── regression-guard/           #   回归防护
    │   ├── plugin-dev/                 #   插件开发指南
    │   ├── feasibility-check/          #   可行性审查
    │   ├── taste-skill/                #   反大厂AI味审美
    │   ├── baseline-ui/                #   UI 基线校验
    │   ├── interaction-completeness/   #   交互完整性审查
    │   ├── docs-writer/                #   技术文档写作
    │   ├── canvas-design/              #   视觉设计创作
    │   ├── long-form-content/          #   长图文生成
    │   ├── pm-*/                       #   50+ 产品管理技能
    │   └── ...
    │
    └── global_workflows/               # 🔄 5 个工作流
        ├── plan.md                     #   /plan — 强制方案审批
        ├── handoff.md                  #   /handoff — 上下文交接
        ├── version.md                  #   /version — 版本管理
        ├── doc-sync-check.md           #   /doc-sync-check — 文档同步检查
        └── layout-engine-check.md      #   /layout-engine-check — 排版引擎检查
```

---

## 🔄 工作流使用指南

在对话中输入 `/命令名` 即可触发对应工作流：

### `/plan` — 计划模式（强制方案审批）
> **何时用**：接到复杂需求、涉及多文件修改、新增模块时

强制 Agent 在写代码前完成方案审批与架构合规检查。流程：
1. 研究现有代码 → 2. 生成 `implementation_plan.md` → 3. 用户审批 → 4. 才能开始编码

### `/handoff` — 上下文交接
> **何时用**：对话过长（20+ 轮）、Agent 表现下降、需要换新对话继续

自动生成交接文档，包含：当前进度、设计决策推理链、否决方案、用户偏好。新对话读取后可无缝继承上下文。

### `/version` — 版本管理
> **何时用**：功能完成、需要提交代码、打版本标签、推送 GitHub

自动执行：`git add` → 生成 Conventional Commit 消息 → `git commit` → 询问是否打 tag → `git push`。支持选择性还原和版本回退。

### `/doc-sync-check` — 文档同步检查
> **何时用**：功能开发完成后、代码审查前

轻量级 7 项检查清单，逐项确认 feature-map、CHANGELOG、architecture.md、AGENTS.md、DSP graph.json、ADR、PLANS.md 是否已同步更新。

### `/layout-engine-check` — 排版引擎检查
> **何时用**：修改排版引擎核心文件时

排版引擎（dom-layout/fabric-mapper/dsl-types 等）变更时的专用检查清单。

## ⚡ 技能分类一览

### 🏗️ 架构与工程（~15 个）

| 技能 | 触发场景 |
|------|---------|
| `harness-gc` | 代码库四维巡检（文档漂移/DSP/死代码/质量） |
| `regression-guard` | 修改代码时防止回归 |
| `plugin-dev` | 开发新插件 |
| `dead-code-sweeper` | 独立清理僵尸代码 |
| `data-structure-protocol` | DSP 图谱导航和维护 |
| `mcp-builder` | 构建 MCP Server |
| `feasibility-check` | 编码前可行性审查 |
| `sdd-plan` | 规格驱动开发计划 |

### 🧪 质量与验证（~8 个）

| 技能 | 触发场景 |
|------|---------|
| `agent-eval` | 四维量化评估 Agent 表现 |
| `code-review` | 六特工联合代码审查 |
| `verification-before-completion` | 交付前强制验证 |
| `test-driven-development` | TDD 红绿重构 |
| `systematic-debugging` | 四阶段系统化调试 |
| `pua` | 反摆烂引擎 + 失败沉淀闭环 |
| `webapp-testing` | Playwright 前端测试 |
| `pr-creator` | PR 创建规范 |

### 🎨 前端与设计（~6 个）

| 技能 | 触发场景 |
|------|---------|
| `taste-skill` | 反大厂 AI 味审美 |
| `baseline-ui` | UI 基线校验 |
| `interaction-completeness` | 交互完整性五态审查 |
| `canvas-design` | 视觉设计创作 |
| `long-form-content` | 长图文排版生成 |
| `react-best-practices` | React 性能 58 条 |

### 📝 文档与交付（~5 个）

| 技能 | 触发场景 |
|------|---------|
| `docs-writer` | 技术文档写作 |
| `docs-changelog` | CHANGELOG 生成 |
| `feature-tracer` | 功能→代码映射归档 |
| `skill-creator` | 创建新技能 |
| `pdf` | PDF 文件处理 |

### 📊 产品管理（50+ 个）

竞品分析、用户画像、定价策略、GTM、OKR、PRD、Sprint 规划、SWOT、波特五力、精益画布、北极星指标等全套 PM 方法论。

---

## 📖 全局规则概览 (`GEMINI.md` v5)

| 章节 | 核心要点 |
|------|---------|
| §1 语言与交互 | 强制中文、禁止占位符、主动技能调度 |
| §2 架构守护 | 可行性审查、DSP 图谱、插件化架构 |
| §3 TDD | 先写测试再写代码、回归守卫、Harness 巡检 |
| §4 前端标准 | 反 AI 味审美、UI 基线、React 性能 |
| §5 环境感知 | 包管理器适配、环境变量保护 |
| §6 调试 | 严禁盲目重试、系统化四阶段诊断 |
| §7 验证交付 | 证据优先于断言、Agent 质量评估、ADR |
| §8 文档工程 | README/CHANGELOG/ADR/版本保护 |
| §9 上下文守护 | 里程碑交接法、跨对话对齐与重建 (Session Hydration) |
| §10 规则路由 | 按任务类型加载规则、环境自举 (Auto-Scaffold) |

---

## 🚀 快速开始

```bash
# 克隆到 Agent 配置目录
git clone https://github.com/yufeileo5-creator/agent-toolkit1.git ~/.gemini

# Agent 会自动加载 GEMINI.md 作为全局规则
# Skills 和 Workflows 按需触发
```

### 项目级配置（可选）

每个项目还可以创建**项目专属**的配置：

```
你的项目/
├── AGENTS.md              # 项目级上下文导航
├── .golden-rules/         # 项目级黄金准则
│   ├── architecture.golden.md
│   ├── code-quality.golden.md
│   ├── documentation.golden.md
│   ├── sandbox-security.golden.md
│   └── error-hints.golden.md
└── PLANS.md               # 持久化设计文档
```

---

## 📜 版本历史

| 版本 | 日期 | 变更 |
| ------ | ---------- | ------------------------------------------------------------ |
| v6 | 2026-03-27 | T0 架构完全体：+ Session Hydration（存在感重建）、+ Auto-Scaffold（环境自举）、+ Non-Interactive CLI 防卡死、+ Revert 熔断机制 |
| v5 | 2026-03-25 | Harness Engineering 全面落地：+harness-gc、+agent-eval、+§10 渐进披露 |
| v4 | 2026-03-20 | 跨对话连续性加固 |
| v3 | 2026-03-19 | 追加插件化全局底座规则 |
| v2 | 2026-03-19 | 增加防摆烂 PUA 显式规则 |
| v1 | 2026-03-19 | 增加版本保护规则完全体 |

---

## 📃 许可

私有配置仓库，仅供个人使用。
