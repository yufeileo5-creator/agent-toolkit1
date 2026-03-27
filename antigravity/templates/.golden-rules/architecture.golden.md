# 架构黄金准则 (Architecture Golden Rules)

> 本文件包含项目架构层面的可检查准则。违反任何一条即为架构退化。

---

## 分层依赖

- [GR-A001] **Core 层禁止导入 Plugin 层**
  → 检查方法: `grep -r "from.*plugins/" src/core/` 应返回空
  → 违规信号: `src/core/` 下的文件出现 `import ... from '../../plugins/...'`
  → 修复方式: 通过 HookRegistry 或 CommandBus 间接通信
  → 来源: 架构初始设计（第一期）

- [GR-A002] **Plugin 间禁止直接 import**
  → 检查方法: 任意 `plugins/X/` 下的文件不应出现 `import ... from '../Y/'`
  → 违规信号: 插件 A 的代码中出现 `from '../pluginB/'`
  → 修复方式: 通过 CommandBus.execute() 或 HookRegistry.tap()/call() 通信
  → 来源: 架构初始设计（第一期）

- [GR-A003] **Types 层零外部依赖**
  → 检查方法: `src/core/types.ts` 不应有 `import` 外部 npm 包的语句
  → 违规信号: types.ts 出现 `import ... from 'fabric'` 等第三方库导入
  → 修复方式: 在 types.ts 中只定义接口和类型，不引用具体实现
  → 来源: 架构初始设计（第一期）

- [GR-A004] **App.tsx 不直接 import Plugin 内部模块**
  → 检查方法: `App.tsx` 不应出现 `import ... from './plugins/X/内部文件'`
  → 违规信号: App.tsx 直接导入插件的内部实现文件
  → 修复方式: 通过 SlotManager 插槽渲染、PluginRegistry 注册
  → 来源: 架构初始设计（第一期）

---

## 命令总线协议

- [GR-A005] **画布操作必须通过 CommandBus**
  → 检查方法: 搜索直接操作 `fabricCanvas` 对象的代码（除 canvas-commands.ts 外）
  → 违规信号: 插件代码中直接调用 `canvas.add()`, `canvas.remove()` 等 Fabric API
  → 修复方式: 封装为注册命令，通过 `context.commands.execute()` 调用
  → 来源: 架构初始设计（第一期）

- [GR-A006] **新增命令必须注册 undo 逻辑**
  → 检查方法: 每个 `registerCommand` 调用必须包含 `undo` 函数
  → 违规信号: 注册了命令但 undo 回调为空函数或缺失
  → 修复方式: 在 execute 回调中保存状态快照，在 undo 回调中恢复
  → 来源: 第三期 undo/redo 系统

---

## 钩子注册协议

- [GR-A007] **核心钩子必须预注册**
  → 检查方法: `hook-registry.ts` 中的 `preRegisteredHooks` 是否包含所有跨插件使用的钩子
  → 违规信号: 插件 A tap 了一个钩子，但该钩子未在 preRegisteredHooks 中声明
  → 修复方式: 在 hook-registry.ts 的 preRegisteredHooks 数组中添加
  → 来源: 第四期插件加载竞态修复

---

## DSP 图谱一致性

- [GR-A008] **新增/删除模块后必须同步 DSP 图谱**
  → 检查方法: `.dsp/graph.json` 中的模块列表与 `src/` 目录结构一致
  → 违规信号: 新增了 `src/plugins/newPlugin/` 但 graph.json 中无对应条目
  → 修复方式: 使用 `dsp-cli` 或手动更新 graph.json
  → 来源: DSP 架构初始化

- [GR-A009] **DSP 图谱的 dependsOn 必须与实际 import 一致**
  → 检查方法: 对比模块文件的 import 语句与 graph.json 的 dependsOn 声明
  → 违规信号: 文件实际 import 了 core/command-bus 但 graph.json 中未声明
  → 修复方式: 更新 graph.json 添加缺失的依赖关系
  → 来源: DSP 架构初始化
