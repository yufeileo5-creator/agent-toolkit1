# 🤖 Agent Toolkit

> Antigravity / Cursor / Gemini CLI 通用的 Agent 技能包 + 全局规则 + 工作流。
> 克隆到任意项目的 `.agents/` 目录即可获得满血配置。

## 快速安装

### 新项目（首次使用）

```powershell
# 1. 克隆到项目根目录的 .agents/ 下
git clone https://github.com/yufeileo5-creator/agent-toolkit1.git .agents

# 2. 安装全局规则 + 初始化 DSP 图谱
.\.agents\setup.ps1
```

### 换电脑（已有项目）

如果项目已经包含 `.agents/`（通过 git submodule 或直接提交），只需要恢复全局规则：

```powershell
.\.agents\setup.ps1
```

## 使用指南 (Usage)

安装完毕后，你可以通过以下两种方式使用 Antigravity Toolkit：

### 1. 显式工作流触发 (斜杠指令)

在聊天框中直接输入以下指令（带斜杠）触发结构化任务：

*   **`/plan [你的需求]`**：强制进入规格设计模式。Agent 不会立刻写代码，而是先调研、出架构方案，产出 `implementation_plan.md` 让你定夺，彻底告别“盲目生成全错代码”。
*   **`/version`**：执行版本管理流。Agent 会扫描文件差异、让你写日志、打 Tag、推送到 GitHub，并把内容记入 `CHANGELOG.md`。

### 2. 隐式技能自动触发 (无感守护)

我们植入了全局规则，Agent 感知到特定场景时会自动调用对应的 Skill，**你不需要输入任何特殊命令**：

*   💡 **新功能可行性拦截 (`feasibility-check`)**：当你提出离谱需求（比如让网页静默录音、访问非授权本地文件），Agent 连代码都不会写，直接亮出 🔴 红灯并给出 B 计划替代方案。
*   🛡️ **防功能退化守卫 (`regression-guard`)**：当你在修改或重构老代码时，Agent 除了改代码，还会强制执行“变更规模分析 -> DSP 图谱依赖查证 -> 回归测试执行”，绝不让你修一个 Bug 引入三个新 Bug。
*   🗑️ **僵尸代码专清 (`dead-code-sweeper`)**：当你输入“扫描没用的代码”，Agent 会启动专门的安全切除流程，不会和其他重构混在一起，防误杀。
*   💅 **前端像素级打磨 (`interaction-completeness`)**：写完页面后，Agent 会顺带把 空态、加载态、错误态、悬停态 给你写齐，不会只管一个正常态就交差。
*   🧪 **测试驱动铁律 (`test-driven-development`)**：修核心逻辑前，你会发现 Agent 坚持非要先写出一段会跑错的 Test，然后再去修你指派的文件。

## 包含内容

### 📐 全局规则
| 文件 | 说明 |
|------|------|
| `GEMINI.md` | 8 大类全局代理约束（中文交互、架构守护、TDD、审美、环境感知、调试、交付验证、文档工程） |

### ⚡ 19 个 Skills

#### 🏗️ 架构与规划
| Skill | 作用 | 来源 |
|-------|------|------|
| [`sdd-plan`](https://agentskill.sh/skills/sdd-plan) | 规格驱动开发，7 阶段 + LLM 裁判 | NeoLabHQ |
| [`data-structure-protocol`](https://agentskill.sh/skills/data-structure-protocol) | 图结构长期代码记忆 | k-kolomeitsev |
| [`mcp-builder`](https://agentskill.sh/@anthropics/mcp-builder) | MCP Server 四阶段开发指南 | Anthropic |

#### 🎨 前端与设计
| Skill | 作用 | 来源 |
|-------|------|------|
| [`taste-skill`](https://agentskill.sh/skills/taste-skill) | 高级前端审美，封杀 AI 通用脸 | Leonxlnx |
| [`react-best-practices`](https://agentskill.sh/skills/react-best-practices) | Vercel 58 条 React 性能规则 | Vercel Labs |
| [`baseline-ui`](https://agentskill.sh/skills/baseline-ui) | Tailwind 动画/排版/无障碍基线 | ibelick |
| [`canvas-design`](https://agentskill.sh/@anthropics/canvas-design) | 视觉设计哲学驱动创作 | Anthropic |
| `interaction-completeness` | 交互完整性七维审查（五态/边界/键盘/拖放/响应式/反馈/文案） | 自定义 |

#### 🧪 测试与验证
| Skill | 作用 | 来源 |
|-------|------|------|
| [`test-driven-development`](https://agentskill.sh/skills/test-driven-development) | TDD 红绿重构铁律 | obra/superpowers |
| [`playwright-skill`](https://agentskill.sh/skills/playwright-skill) | 50+ 生产级 E2E 测试模式 | testdino-hq |
| [`webapp-testing`](https://agentskill.sh/@anthropics/webapp-testing) | Playwright Web 应用端到端测试 | Anthropic |
| [`verification-before-completion`](https://agentskill.sh/skills/verification-before-completion) | 交付前强制验证 | obra/superpowers |

#### 🔍 调试、审计与审查
| Skill | 作用 | 来源 |
|-------|------|------|
| `feasibility-check` | 功能新开前的硬技术边界扫描（防天坑第一步） | 自定义 |
| `regression-guard` | 强制回归防退化（Git Diff/导入链/视觉全系测试） | 自定义 |
| `dead-code-sweeper` | 独立原子化的僵尸代码/冗余依赖专清任务 | 自定义 |
| [`systematic-debugging`](https://agentskill.sh/skills/systematic-debugging) | 四阶段系统调试 | obra/superpowers |
| [`code-review`](https://agentskill.sh/@google-gemini/code-reviewer) | 6 专家联合代码审查 | NeoLabHQ |

#### 📚 文档与交付
| Skill | 作用 | 来源 |
|-------|------|------|
| [`docs-writer`](https://agentskill.sh/@google-gemini/docs-writer) | 四阶段技术文档写作 | Google Gemini |
| [`docs-changelog`](https://agentskill.sh/@google-gemini/docs-changelog) | 变更日志生成与维护 | Google Gemini |
| [`pr-creator`](https://agentskill.sh/@google-gemini/pr-creator) | 高质量 PR 创建规范 | Google Gemini |
| [`pdf`](https://agentskill.sh/@anthropics/pdf) | PDF 全功能处理（读取/合并/OCR 等） | Anthropic |
| [`skill-creator`](https://agentskill.sh/@google-gemini/skill-creator) | Agent Skill 创建与优化指南 | Google Gemini |

### 🔄 工作流
| 文件 | 说明 |
|------|------|
| `workflows/plan.md` | 强制计划模式，修改代码前必须出方案并等用户批准 |
| `workflows/version.md` | 使用 `/version` 触发的一键版本管理（标签、提交、推送、Changelog） |

## 文件结构

```
.agents/
├── GEMINI.md              # 全局规则（安装脚本会复制到 ~/.gemini/）
├── README.md              # 本文件
├── setup.ps1              # 一键安装脚本
├── skills/
│   ├── baseline-ui/          # Tailwind 基线
│   ├── canvas-design/        # 视觉设计创作
│   ├── code-review/          # 代码审查
│   ├── data-structure-protocol/  # DSP 图谱
│   ├── dead-code-sweeper/    # 僵尸代码专清
│   ├── docs-changelog/       # 变更日志
│   ├── docs-writer/          # 技术文档写作
│   ├── feasibility-check/    # 可行性与硬边界审查
│   ├── mcp-builder/          # MCP 开发
│   ├── pdf/                  # PDF 处理
│   ├── playwright-skill/     # E2E 测试模式
│   ├── pr-creator/           # PR 创建
│   ├── react-best-practices/ # React 性能
│   ├── regression-guard/     # 核心防退化回归守卫
│   ├── sdd-plan/             # 规格驱动开发
│   ├── skill-creator/        # Skill 创建
│   ├── systematic-debugging/ # 系统调试
│   ├── taste-skill/          # 前端审美
│   ├── test-driven-development/  # TDD
│   ├── verification-before-completion/  # 交付验证
│   └── webapp-testing/       # Web 应用测试
└── workflows/
    ├── plan.md
    └── version.md
```

## 更新

```powershell
cd .agents
git pull origin main
```
