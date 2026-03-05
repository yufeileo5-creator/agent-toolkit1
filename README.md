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
| `GEMINI.md` | 7 大类全局代理约束（中文交互、架构守护、TDD、审美、调试、交付验证） |

### ⚡ 10 个 Skills
| Skill | 作用 | 来源 |
|-------|------|------|
| `sdd-plan` | 规格驱动开发，7 阶段 + LLM 裁判 | NeoLabHQ |
| `code-review` | 6 专家联合代码审查 | NeoLabHQ |
| `systematic-debugging` | 四阶段系统调试 | obra/superpowers |
| `taste-skill` | 高级前端审美，封杀 AI 通用脸 | Leonxlnx |
| `react-best-practices` | Vercel 58 条 React 性能规则 | Vercel Labs |
| `baseline-ui` | Tailwind 动画/排版/无障碍基线 | ibelick |
| `verification-before-completion` | 交付前强制验证 | obra/superpowers |
| `playwright-skill` | 50+ 生产级 E2E 测试模式 | testdino-hq |
| `test-driven-development` | TDD 红绿重构铁律 | obra/superpowers |
| `data-structure-protocol` | 图结构长期代码记忆 | k-kolomeitsev |

### 🔄 工作流
| 文件 | 说明 |
|------|------|
| `workflows/plan.md` | 强制计划模式，修改代码前必须出方案并等用户批准 |

## 文件结构

```
.agents/
├── GEMINI.md              # 全局规则（安装脚本会复制到 ~/.gemini/）
├── README.md              # 本文件
├── skills/
│   ├── baseline-ui/
│   ├── code-review/
│   ├── data-structure-protocol/
│   ├── playwright-skill/
│   ├── react-best-practices/
│   ├── sdd-plan/
│   ├── systematic-debugging/
│   ├── taste-skill/
│   ├── test-driven-development/
│   └── verification-before-completion/
└── workflows/
    └── plan.md
```

## 更新

```powershell
cd .agents
git pull origin main
```
