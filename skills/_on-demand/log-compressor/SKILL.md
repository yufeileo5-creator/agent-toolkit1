---
name: log-compressor
description: 上下文降噪卫士。当遭遇包含海量报错（>50行）、依赖包堆栈、或编译/测试失败的终端输出时强制触发。对日志执行手术刀级剪裁，防止大段无用文本冲垮记忆窗口。
---
# 🧹 Log Compressor (终端噪音熔断守卫)

**核心使命**：成为大模型（你自己）的“上下文窗口降噪阀”。在面临超长控制台输出时，坚决抵制“全量裸读”，必须将庞杂数据压缩至少 80% 后再做推理。

## 🎯 触发条件
1. 执行了构建 (`npm run build`)、全量测试 (`npx vitest run`) 或第三方库安装，且控制台输出明显超过一屏。
2. 捕获到深层级联的 React 报错树或 Node.js `node_modules` 内部堆栈。
3. 从其它组件获取到了大段混杂着普通 Info 级别日志的 Error Report。

## ⚔️ 压缩铁律 (Compression Protocols)

### 1. 拒绝直读终端 (I/O Redirection)
当你知道某个命令（如 `vitest run` 或 `build`）可能产生万行日志时：
- **禁止**：直接在 CLI 里敲命令并让结果回显到标准终端输出。
- **必须**：通过重定向符写文件：`npx vitest run > /tmp/error.log 2>&1`。然后改用文本检索工具。

### 2. 手术刀提纯 (Surgical Extraction)
使用 `grep_search` 工具去寻找以下核心指纹：
- **致命标识**: 仅过滤包含 `ERR!` / `FAIL` / `Exception` / `SyntaxError` / `TypeError` 及其上下文的行。
- **业务溯源**: 直接无视所有落入 `node_modules/...` 甚至 `node:internal/...` 的底层抛单路径，只提取第一条从**当前项目源码**（如 `src/...` 或 `server/...`）里冒出来的最顶层调用堆栈！

### 3. 构建微型降噪简报 (Micro-Briefing)
在读取完错误后，不要向用户或上下文中输出巨大的原生长日志。你必须首先在脑中总结出一个高度结构化的微型简报：
> 示例："发现 24 处错误。已剔除 React 内部链路。根本原因(Root Cause)收敛于 `src/components/List.tsx:L42`。正在寻找修复方案。"

## ⚠️ 避坑提示 (Gotchas)
- **首部爆窗陷阱**：如果不使用 `> /tmp/error.log` 重定向，极长日志会在终端监控工具栈里被操作系统或接口粗暴截断，导致你**刚好丢失掉报错头部（真正的源头位置 Root Cause）**。
- **盲目重试陷阱**：有些框架日志很长是因为连串的 `Warning`，压缩期间必须严格判定，只锁死 `Error`，过滤噪音。
