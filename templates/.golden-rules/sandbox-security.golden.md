# 沙箱安全守护准则 (Sandbox Security Golden Rules)

> 本文件包含沙箱安全和文件操作边界的可检查准则。
> 当前阶段为轻量化防护（本地开发环境），SaaS 化后需升级为进程级隔离。

---

## 文件操作边界

- [GR-S001] **Agent 只能修改项目目录内的文件**
  → 检查方法: 所有 write_to_file / replace_file_content 的目标路径必须在 `<项目根目录>\` 或 Agent 全局配置目录内
  → 违规信号: Agent 修改了 `C:\Windows\`、`C:\Program Files\` 等系统目录
  → 修复方式: 限制文件操作的目标路径
  → 来源: Harness Engineering — Sandbox 组件

- [GR-S002] **禁止删除项目根目录的关键文件**
  → 检查方法: 以下文件不得被删除：`package.json`、`tsconfig.json`、`.env`、`AGENTS.md`、`.dsp/graph.json`
  → 违规信号: Agent 执行了 `rm` 或删除操作影响关键文件
  → 修复方式: 在所有涉及文件删除的操作前做路径检查
  → 来源: Harness Engineering — Sandbox 组件

---

## 敏感信息保护

- [GR-S003] **API Key 严禁硬编码**
  → 检查方法: `grep -r "sk-ant\|sk-proj\|AIzaSy" src/ server/` 应返回空
  → 违规信号: 源码中出现 API Key 或 Secret 的实际值
  → 修复方式: 使用 `.env` 注入，通过 `process.env.XXX` 读取
  → 来源: 全局规则 / 安全基线

- [GR-S004] **.env 文件必须在 .gitignore 中**
  → 检查方法: `.gitignore` 中包含 `.env` 条目
  → 违规信号: `.env` 被提交到版本控制
  → 修复方式: 在 `.gitignore` 中添加 `.env`，从 git 历史中移除
  → 来源: 安全基线

- [GR-S005] **新增环境变量必须同步 .env.example**
  → 检查方法: `.env.example` 中的变量集合是 `.env` 的超集（除了实际值外）
  → 违规信号: `.env` 中有变量但 `.env.example` 中没有对应条目
  → 修复方式: 在 `.env.example` 中添加变量名和注释说明
  → 来源: 全局规则

---

## 网络请求边界

- [GR-S006] **前端代码禁止直接调用外部 API**
  → 检查方法: `src/` 下的文件不应出现直接的 `fetch('https://api.anthropic.com/...')` 等外部 API 调用
  → 违规信号: 插件代码中直接调用第三方 API（跳过 BFF 层）
  → 修复方式: 所有外部 API 调用必须通过 `server/routes/` BFF 代理
  → 来源: 架构分层 / 安全基线

- [GR-S007] **BFF 层拥有速率限制**
  → 检查方法: `server/routes/ai.ts` 中使用了 `express-rate-limit`
  → 违规信号: 新增的 API 路由缺少速率限制
  → 修复方式: 对高频 / 高成本端点配置 rate-limit 中间件
  → 来源: BFF 安全基线

---

## 执行隔离（SaaS 化时启用）

- [GR-S008] **[预留] 用户上传文件的沙箱隔离**
  → 当前状态: 未实施（本地开发环境不需要）
  → 未来需求: 用户上传的文件必须在隔离的临时目录中处理，处理完毕后清理
  → 触发条件: 项目走向多用户 SaaS 部署时

- [GR-S009] **[预留] Agent 执行命令的沙箱限制**
  → 当前状态: 未实施
  → 未来需求: Agent 执行的终端命令应限制在 allowlist 中，禁止 `rm -rf /`、`shutdown` 等危险命令
  → 触发条件: Agent 在生产环境中自主运行时
