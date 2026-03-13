# Changelog

本文件记录 Agent Toolkit 的所有版本变更。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

---

## [v1.2.0] - 2026-03-09

### 新增
- **interaction-completeness** skill — 自定义交互完整性审查（7 大检查维度）
  - 五态完整性（空/加载/错误/成功/禁用）
  - 边界条件（超长内容/极端数值/快速操作/网络异常）
  - 键盘与焦点（Tab 顺序/ESC 关闭/焦点陷阱）
  - 拖放与画布（边界/缩放极限/撤销重做/碰撞检测）
  - 响应式适配（触摸区域/断点行为/虚拟键盘）
  - 过渡与反馈（确认提示/未保存提醒/进度指示）
  - 文案与提示（错误信息/空状态引导/Tooltip）

### 变更
- `GEMINI.md`：第 4 节新增 interaction-completeness 触发规则
- `README.md`：18 → 19 Skills，新增交互完整性条目
- `setup.ps1`：更新 Skills 数量

---

## [v1.1.1] - 2026-03-09

### 变更
- 全部 18 个 Skills 的 YAML description 字段从英文汉化为中文
- `/` 菜单说明全面中文化，提升中文用户的匹配体验

---

## [v1.1.0] - 2026-03-09

### 新增
- 8 个新 Skills：

  **来自 Anthropic ([agentskill.sh](https://agentskill.sh))：**
  - [`canvas-design`](https://agentskill.sh/@anthropics/canvas-design) — 视觉设计哲学驱动创作
  - [`mcp-builder`](https://agentskill.sh/@anthropics/mcp-builder) — MCP Server 四阶段开发指南
  - [`pdf`](https://agentskill.sh/@anthropics/pdf) — PDF 全功能处理
  - [`webapp-testing`](https://agentskill.sh/@anthropics/webapp-testing) — Playwright Web 应用测试

  **来自 Google Gemini ([agentskill.sh](https://agentskill.sh))：**
  - [`pr-creator`](https://agentskill.sh/@google-gemini/pr-creator) — PR 创建规范
  - [`docs-writer`](https://agentskill.sh/@google-gemini/docs-writer) — 四阶段技术文档写作
  - [`docs-changelog`](https://agentskill.sh/@google-gemini/docs-changelog) — 变更日志生成维护
  - [`skill-creator`](https://agentskill.sh/@google-gemini/skill-creator) — Skill 创建与优化指南

### 变更
- `GEMINI.md`：从 7 大类扩展为 8 大类规则，新增 8 条 skill 触发引用
  - §1 新增 skill-creator
  - §2 新增 mcp-builder
  - §4 新增 canvas-design
  - §7 新增 webapp-testing、pr-creator
  - §8（新增）文档工程：docs-writer、docs-changelog、pdf
- `README.md`：10 → 18 Skills，按功能分类，含 agentskill.sh 可点击链接
- `setup.ps1`：更新 Skills 数量

---

## [v1.0.0] - 2026-03-09

### 初始发布
- **全局规则** (`GEMINI.md`)：7 大类全局代理约束
  - 中文交互、架构守护、TDD、审美、环境感知、系统化调试、交付验证
- **10 个 Skills：**
  - `sdd-plan` — 规格驱动开发 (NeoLabHQ)
  - `code-review` — 6 专家联合代码审查 (NeoLabHQ)
  - `systematic-debugging` — 四阶段系统调试 (obra/superpowers)
  - `taste-skill` — 高级前端审美 (Leonxlnx)
  - `react-best-practices` — Vercel 58 条 React 性能规则 (Vercel Labs)
  - `baseline-ui` — Tailwind 动画/排版/无障碍基线 (ibelick)
  - `verification-before-completion` — 交付前强制验证 (obra/superpowers)
  - `playwright-skill` — 50+ 生产级 E2E 测试模式 (testdino-hq)
  - `test-driven-development` — TDD 红绿重构铁律 (obra/superpowers)
  - `data-structure-protocol` — 图结构长期代码记忆 (k-kolomeitsev)
- **工作流**：`workflows/plan.md` — 强制计划模式
- **安装脚本**：`setup.ps1` — 一键安装全局规则 + DSP 初始化

---

[v1.2.0]: https://github.com/yufeileo5-creator/agent-toolkit1/compare/v1.1.1...v1.2.0
[v1.1.1]: https://github.com/yufeileo5-creator/agent-toolkit1/compare/v1.1.0...v1.1.1
[v1.1.0]: https://github.com/yufeileo5-creator/agent-toolkit1/compare/v1.0.0...v1.1.0
[v1.0.0]: https://github.com/yufeileo5-creator/agent-toolkit1/releases/tag/v1.0.0
