# 错误自修复提示模板 (AGENT_HINT Error Templates)

> 本文件定义常见错误场景的 AGENT_HINT 自修复提示模板。
> 当 Agent 遇到这些错误时，应参考此处的提示自动修复，而非从零排查。
>
> **未来演进**: 这些模板最终应嵌入到 `health-monitor.ts` 或 Vite 错误回调中，使错误消息自带修复指引。

---

## Fabric.js 相关

### SecurityError: Tainted Canvas
```
❌ 原始错误: "Failed to execute 'toDataURL' on 'HTMLCanvasElement': Tainted canvases may not be exported."

[AGENT_HINT] 画布被跨域图片污染。检查 canvas-commands.ts 中的图片加载是否设置了 crossOrigin: 'anonymous'。
如果图片源不支持 CORS，需要通过 BFF 代理下载图片。
参考: src/plugins/canvas-engine/canvas-commands.ts → addImage 命令
参考: docs/architecture.md → Tainted Canvas 安全降级
```

### fabric is not defined
```
❌ 原始错误: "ReferenceError: fabric is not defined"

[AGENT_HINT] FabricFactory 使用延迟初始化（import('fabric')），在 onCanvasReady 回调之前不可用。
确保在 FabricFactory 初始化完成后才调用 Fabric API。
参考: src/plugins/canvas-engine/AGENTS.md → Fabric.js 相关
```

---

## Yoga WASM 相关

### Yoga module not found
```
❌ 原始错误: "Error: Cannot find module 'yoga-layout'"

[AGENT_HINT] Yoga WASM 模块需要正确安装。运行 npm install 检查 yoga-layout 是否在 dependencies 中。
在 Vitest 环境中，可能需要 mock yoga-bridge.ts。
参考: src/plugins/canvas-engine/yoga-bridge.ts
```

---

## 命令总线相关

### Command not found
```
❌ 原始错误: "Error: Command 'canvas:xxx' not found"

[AGENT_HINT] 命令未注册。检查对应插件的 activate() 函数中是否调用了 context.commands.registerCommand()。
插件加载顺序可能导致命令尚未注册——确认是否需要在 HookRegistry 中预注册钩子。
参考: src/core/command-bus.ts → registerCommand()
参考: .golden-rules/architecture.golden.md → GR-A007
```

### Undo stack empty
```
❌ 原始错误: "Warning: Undo stack is empty, nothing to undo"

[AGENT_HINT] 这不是错误，是正常行为。但如果用户执行了操作后仍提示空栈，
检查 registerCommand 时是否提供了 undo 回调函数（参见 GR-A006）。
```

---

## 插件系统相关

### Plugin activation failed
```
❌ 原始错误: "Error: Plugin 'xxx' activation failed"

[AGENT_HINT] 检查插件的 activate(context) 函数。常见原因：
1. 依赖的钩子未预注册（参见 hook-registry.ts preRegisteredHooks）
2. 依赖的命令由其他插件注册，但该插件尚未加载（Promise.all 竞态）
3. activate 中的异步操作未 await
参考: src/core/plugin-manager.ts → loadPlugins()
```

### Slot render error
```
❌ 原始错误: "Error: Failed to render slot 'xxx'"

[AGENT_HINT] SlotManager 有 ErrorBoundary 隔离，单个插槽崩溃不影响其他插槽。
检查注入到该插槽的 React 组件是否有运行时错误。
参考: src/core/slot-manager.ts
```

---

## BFF / API 相关

### Rate limit exceeded
```
❌ 原始错误: "429 Too Many Requests"

[AGENT_HINT] BFF 层有 express-rate-limit 限制（20次/15分钟）。
如果是开发调试，可在 server/routes/ai.ts 中临时调大限制。
生产环境应保持限制或对不同端点设置不同阈值。
```

### API Key missing
```
❌ 原始错误: "Error: ANTHROPIC_API_KEY is not set"

[AGENT_HINT] API Key 通过 .env 文件注入。检查：
1. .env 文件是否存在且包含 ANTHROPIC_API_KEY=sk-...
2. .env 文件是否在项目根目录（不是 server/ 子目录）
3. vite / express 是否正确加载了 dotenv
参考: .env.example
```

---

## 构建 / 编译相关

### Module not found
```
❌ 原始错误: "Error: Module not found: ./xxx"

[AGENT_HINT] 文件路径可能在重构中发生了变化。使用 find_by_name 或 grep_search 搜索目标文件的实际位置。
如果是 core/ 下的模块，检查 docs/architecture.md 获取最新结构。
如果是 plugins/ 下的模块，检查对应插件目录的 AGENTS.md。
```

### Type error after refactor
```
❌ 原始错误: "Type 'X' is not assignable to type 'Y'"

[AGENT_HINT] 类型定义可能已更新但调用方未同步。检查 src/core/types.ts 获取最新的类型定义。
使用 tsc --noEmit 查看所有类型错误的完整列表。
```
