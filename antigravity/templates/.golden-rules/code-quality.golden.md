# 代码质量黄金准则 (Code Quality Golden Rules)

> 本文件包含代码质量层面的可检查准则。每次代码修改后应逐条自检。

---

## 类型安全

- [GR-Q001] **禁用 any 类型**
  → 检查方法: `grep -r ": any" src/` 应返回空（测试文件除外）
  → 违规信号: 业务代码中出现 `: any`, `as any`, `<any>`
  → 修复方式: 定义具体接口或使用 `unknown` + 类型守卫
  → 来源: 全局规则 / TypeScript 严格模式

- [GR-Q002] **所有公共 API 必须有 TSDoc**
  → 检查方法: `export function` / `export interface` 前必须有 `/** ... */` 注释
  → 违规信号: 导出的函数或接口没有文档注释
  → 修复方式: 添加 TSDoc，包含参数说明、返回值、异常情况
  → 来源: 文档工程规则

---

## 函数与文件长度

- [GR-Q003] **核心逻辑函数 ≤ 40 行**
  → 检查方法: 统计函数体行数（不含空行和注释）
  → 违规信号: 单个函数的逻辑代码超过 40 行
  → 修复方式: 提取辅助函数、使用策略模式或管道模式拆分
  → 来源: 全局规则

- [GR-Q004] **常规文件 ≤ 300 行**
  → 检查方法: `wc -l <文件>` 不超过 300
  → 违规信号: 文件总行数超过 300 行
  → 修复方式: 按职责拆分为多个文件，提取公共逻辑
  → 来源: 全局规则

---

## 防御性编码

- [GR-Q005] **所有外部输入必须校验**
  → 检查方法: API 路由处理函数、文件读取结果、用户输入不能直接使用
  → 违规信号: `req.body.xxx` 直接使用而无类型检查或校验
  → 修复方式: 使用校验库（如 zod）或手写类型守卫
  → 来源: 全局规则

- [GR-Q006] **异步操作必须有错误处理**
  → 检查方法: 所有 `await` 调用必须在 `try/catch` 中或有 `.catch()` 处理
  → 违规信号: 裸 `await` 调用没有错误处理
  → 修复方式: 添加 try/catch 并上报 HealthMonitor 或向用户显示错误
  → 来源: 第五期 Tainted Canvas 异常处理教训

---

## 导入规范

- [GR-Q007] **导入顺序**
  → 检查方法: 导入语句按以下顺序排列，组间空行分隔
  → 违规信号: 导入混乱，第三方库和相对路径混在一起
  → 修复方式:
    ```
    // 1. 外部库
    import { SyncHook } from 'tapable';
    
    // 2. 核心模块
    import type { PluginContext } from '../../core/types';
    
    // 3. 同目录/相对路径
    import { canvasCommands } from './canvas-commands';
    ```
  → 来源: 代码风格规则

---

## 命名规范

- [GR-Q008] **变量/函数使用 camelCase**
  → 检查方法: 检查变量和函数声明的命名格式
  → 违规信号: `my_variable`, `MyFunction`（函数不应用 PascalCase）
  → 修复方式: 统一为 camelCase
  → 来源: 代码风格规则

- [GR-Q009] **类型/接口/组件使用 PascalCase**
  → 检查方法: 检查 type, interface, React 组件的命名格式
  → 违规信号: `pluginContext`（接口名）、`healthBar`（组件名）
  → 修复方式: 统一为 PascalCase
  → 来源: 代码风格规则
