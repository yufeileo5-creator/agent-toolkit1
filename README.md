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
| `workflows/layout-engine-check.md` | 用于前端排版核心变更时的安全检查单 |

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
    ├── layout-engine-check.md
    └── version.md
```

## 更新

```powershell
cd .agents
git pull origin main
```
