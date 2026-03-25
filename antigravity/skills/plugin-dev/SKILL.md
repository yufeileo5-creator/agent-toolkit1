---
name: plugin-dev
description: 插件开发技能——AI 开发新插件时自动加载，提供标准目录结构、接口协议、注册方式等完整指导
---

# 插件开发 Skill

> 当 AI 需要创建或修改插件时，必须严格按照本 Skill 执行。

## 插件分类

| 类型 | scope 值 | 加载时机 |
|------|----------|---------|
| **共享插件** | `'shared'` | 所有项目类型都加载 |
| **类型专属插件** | `ProjectType`（如 `'ui-app'`） | 仅对应 ProjectType 加载 |

## 标准目录结构

```
src/plugins/{plugin-id}/
├── index.ts           # 插件入口，导出 default Plugin 实例
├── manifest.ts        # 插件清单，声明 id/name/version/scope
└── __tests__/
    └── index.test.ts  # 单元测试（TDD 先行）
```

## 开发流程（严格 TDD）

### Step 1: 创建清单

```typescript
// manifest.ts
import type { PluginManifest } from '@/core/types';

const manifest: PluginManifest = {
  id: 'my-plugin',
  name: 'My Plugin',
  version: '1.0.0',
  scope: 'shared', // 或具体的 ProjectType
  description: '插件描述',
};

export default manifest;
```

### Step 2: 先写测试（RED）

```typescript
// __tests__/index.test.ts
import { describe, it, expect } from 'vitest';
import myPlugin from '../index';
import { createHookRegistry } from '@/core/hook-registry';
import { createCommandBus } from '@/core/command-bus';
import { createSlotManager } from '@/core/slot-manager';
import { createHealthMonitor } from '@/core/health-monitor';
import type { PluginContext } from '@/core/types';

function createTestContext(): PluginContext {
  return {
    hooks: createHookRegistry(),
    commands: createCommandBus(),
    slots: createSlotManager(),
    health: createHealthMonitor(),
  };
}

describe('MyPlugin', () => {
  it('manifest 应包含正确的元信息', () => {
    expect(myPlugin.manifest.id).toBe('my-plugin');
    expect(myPlugin.manifest.scope).toBe('shared');
  });

  it('激活后应注册命令', () => {
    const ctx = createTestContext();
    myPlugin.activate(ctx);
    // 断言注册了预期的命令...
  });
});
```

### Step 3: 实现插件（GREEN）

```typescript
// index.ts
import type { Plugin, PluginContext } from '@/core/types';
import manifest from './manifest';

const myPlugin: Plugin = {
  manifest,

  activate(context: PluginContext) {
    // 1. 监听钩子
    context.hooks.tap('some:hook', 'my-plugin', (data) => { ... });

    // 2. 注册命令
    context.commands.register('my-plugin:action', {
      execute: (payload) => { ... },
      undo: () => { ... }, // 可选
    });

    // 3. 注入 UI 组件
    context.slots.inject('main-content', {
      id: 'my-plugin-widget',
      component: MyComponent,
      order: 50,
    });

    // 4. 上报健康状态
    context.health.report('my-plugin', 'healthy');
  },

  deactivate() {
    // 清理资源
  },
};

export default myPlugin;
```

### Step 4: 注册到注册表

在 `src/core/plugin-registry.ts` 中添加：

```typescript
// pluginRegistry 数组中添加
{ id: 'my-plugin', loader: () => import('@/plugins/my-plugin') },
```

如果是共享插件，还要加到 `sharedPlugins` 数组。
如果是类型专属插件，加到 `typePlugins[对应Type]` 数组。

## 接口要求

- 必须实现 `Plugin` 接口（`manifest` + `activate` + `deactivate`）
- `activate` 接收 `PluginContext`，通过它访问钩子/命令/插槽/健康
- `deactivate` 必须清理所有资源

## 样式规范

- 使用 Tailwind 类名 + `@layer plugin-{pluginId}` 命名空间
- 禁止全局裸 CSS
- 禁止覆盖其他插件的样式

## 禁止事项

- ❌ **禁止 `import` 其他业务插件的代码**（插件间完全瞎子级隔离，只准通过 `CommandBus` 和 `Hook` 通信）。
- ❌ 禁止静态 `import` 写死在 `main.tsx`。对于携带如图表等巨型依赖的重量级插件，**强制使用动态导入（Dynamic Import / 懒加载）** 在 `pluginRegistry` 中注册，严禁拖慢主包体积。
- ❌ 禁止写全局裸 CSS。
- ❌ **严禁跨域操作状态**：严禁直接改变其他插件的状态，严禁操作全局 Zustand store 的非公开字段。
- ❌ 禁止在 `core/` 目录下添加任何业务功能代码。
