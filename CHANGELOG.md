# Changelog

所有 Agent Toolkit 的版本变更记录。格式遵循 [Keep a Changelog](https://keepachangelog.com/)。

---

## [v1.2.0] - 2026-03-09

### 新增
- **interaction-completeness** skill — 交互完整性七维审查（自定义）
  - 五态完整性（空/加载/错误/成功/禁用）
  - 边界条件（超长内容/极端数值/快速操作/网络异常）
  - 键盘与焦点（Tab 顺序/ESC 关闭/焦点陷阱）
  - 拖放与画布（边界限制/缩放极限/撤销重做）
  - 响应式适配（触摸区域/断点/虚拟键盘）
  - 过渡与反馈（确认框/未保存提醒/进度指示）
  - 文案与提示（错误信息/空状态引导/Tooltip）

### 变更
- `GEMINI.md` 第 4 节新增 interaction-completeness 触发规则
- `README.md` / `setup.ps1` 更新为 19 个 Skills
- 引入 git tag 版本管理机制

---

## [v1.1.1] - 2026-03-09

### 变更
- 全部 18 个 Skills 的 YAML `description` 字段从英文汉化为中文
- `/` 菜单说明现在全部显示中文

---

## [v1.1.0] - 2026-03-09

### 新增
- **canvas-design** skill — 视觉设计哲学驱动创作（来源：Anthropic）
- **mcp-builder** skill — MCP Server 四阶段开发指南（来源：Anthropic）
- **pdf** skill — PDF 全功能处理（来源：Anthropic）
- **webapp-testing** skill — Playwright Web 应用测试（来源：Anthropic）
- **pr-creator** skill — PR 创建规范（来源：Google Gemini）
- **docs-writer** skill — 四阶段技术文档写作（来源：Google Gemini）
- **docs-changelog** skill — 变更日志生成与维护（来源：Google Gemini）
- **skill-creator** skill — Agent Skill 创建指南（来源：Google Gemini）

### 变更
- `GEMINI.md` 更新为 8 大类规则，新增第 8 节"文档工程"
- `GEMINI.md` 第 1/2/4/7/8 节新增 8 条 skill 触发引用
- `README.md` 重写为分类展示（18 Skills），每个 skill 含 agentskill.sh 可点击链接
- `setup.ps1` 更新为 18 个 Skills

---

## [v1.0.0] - 2026-03-06

### 初始发布
包含 10 个 Skills + 全局规则 + 计划工作流。

#### Skills
| Skill | 来源 |
|-------|------|
| `sdd-plan` | NeoLabHQ |
| `code-review` | NeoLabHQ |
| `systematic-debugging` | obra/superpowers |
| `taste-skill` | Leonxlnx |
| `react-best-practices` | Vercel Labs |
| `baseline-ui` | ibelick |
| `verification-before-completion` | obra/superpowers |
| `playwright-skill` | testdino-hq |
| `test-driven-development` | obra/superpowers |
| `data-structure-protocol` | k-kolomeitsev |

#### 规则
- `GEMINI.md` — 7 大类全局代理约束

#### 工作流
- `workflows/plan.md` — 强制计划模式
