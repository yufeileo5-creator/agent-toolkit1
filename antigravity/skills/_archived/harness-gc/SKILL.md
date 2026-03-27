---
name: harness-gc
description: >-
  Harness 垃圾回收巡检技能。定期扫描代码库四大维度（文档漂移、DSP 图谱一致性、死代码、依赖审计），
  用 Golden Principles 作为判定标准，输出健康报告和修复建议。
  触发场景：项目维护、代码审查、架构治理、「巡检」「清理」「一致性检查」「harness gc」等。
---

# Harness GC — 代码库垃圾回收巡检

定期扫描代码库，对抗 AI 生成代码的质量退化和文档漂移。基于 `.golden-rules/` 中的黄金准则作为判定标准。

## 触发时机

- 用户主动触发：`/harness-gc`、「做一次巡检」、「检查代码库健康度」
- 建议性触发：连续开发 3+ 个功能后、跨期交接前、重大重构后
- `pua` 技能失败沉淀后的自动延伸检查

## 前置条件

- 项目根目录存在 `.golden-rules/` 目录
- 项目根目录存在 `.dsp/graph.json`
- 项目根目录存在 `docs/feature-map.md`

## 巡检流程

### 阶段 1：文档漂移检测

按 `.golden-rules/documentation.golden.md` 中的 GR-D001 ~ GR-D009 逐条检查：

1. **feature-map 一致性**
   - 解析 `docs/feature-map.md` 中的所有文件路径引用
   - 验证每个引用的文件是否实际存在
   - 检查 `src/plugins/` 下是否有未被 feature-map 覆盖的插件
   - 输出：过时条目列表 + 未覆盖功能列表

2. **architecture.md 一致性**
   - 对比 `docs/architecture.md` 中的 Mermaid 图与实际目录结构
   - 检查模块名、文件名是否匹配
   - 输出：不一致项列表

3. **AGENTS.md 一致性**
   - 对比根目录 `AGENTS.md` 的项目结构描述与实际目录
   - 检查子目录 AGENTS.md 是否与对应模块结构一致
   - 输出：过时描述列表

4. **CHANGELOG 完整性**
   - 检查最近的 git commits 是否有对应的 CHANGELOG 条目
   - 输出：缺失条目的 commit 列表

### 阶段 2：DSP 图谱校验

按 `.golden-rules/architecture.golden.md` 中的 GR-A008 ~ GR-A009 检查：

1. **模块存在性**
   - 解析 `.dsp/graph.json` 中的所有模块条目
   - 验证每个模块对应的文件/目录是否存在
   - 检查 `src/` 下是否有未在图谱中声明的模块
   - 输出：幽灵模块列表 + 未追踪模块列表

2. **依赖方向校验**
   - 按 GR-A001 ~ GR-A004 检查实际 import 是否违反分层规则
   - 执行：`grep -r "from.*plugins/" src/core/` 检查反向依赖
   - 检查插件间是否存在直接 import
   - 输出：违规 import 列表

3. **dependsOn 一致性**
   - 对比模块文件的实际 import 与 graph.json 声明的 dependsOn
   - 输出：缺失依赖声明 + 多余依赖声明

### 阶段 3：死代码扫描

> 本阶段调用 `dead-code-sweeper` 技能的核心逻辑，但不执行删除操作。

1. 扫描未使用的导出（exported but never imported）
2. 扫描未使用的依赖（package.json 中声明但未 import 的包）
3. 扫描空文件或只有 import 的文件
4. 输出：可疑死代码清单（仅报告，不删除）

### 阶段 4：代码质量抽检

按 `.golden-rules/code-quality.golden.md` 抽样检查：

1. **any 类型扫描**: `grep -r ": any" src/ --include="*.ts" --include="*.tsx"`（排除测试文件和 .d.ts）
2. **超长函数抽检**: 随机抽取 5 个核心文件，检查函数长度
3. **裸 await 扫描**: 检查是否有未 try/catch 的异步操作
4. 输出：质量问题清单

## 输出格式

```markdown
# 🧹 Harness GC 巡检报告

> 扫描时间: YYYY-MM-DD HH:mm
> 扫描范围: [完整/增量]

## 📊 健康度评分

| 维度 | 评分 | 问题数 |
|------|------|--------|
| 文档一致性 | 🟢/🟡/🔴 | N |
| DSP 图谱 | 🟢/🟡/🔴 | N |
| 死代码 | 🟢/🟡/🔴 | N |
| 代码质量 | 🟢/🟡/🔴 | N |

## 🔴 必须修复（阻断性问题）
...

## 🟡 建议修复（质量退化信号）
...

## 🟢 健康项（无需处理）
...

## 📋 修复建议
1. [具体修复步骤]
```

## 最佳实践

- ✅ 巡检后将发现的新规律沉淀为 `.golden-rules/` 中的新准则
- ✅ 严重问题应创建独立的修复任务，不要在巡检过程中直接修复
- ✅ 增量巡检时只关注最近变更涉及的文件
- ❌ 不要在巡检中"顺便"删除死代码（触发 `dead-code-sweeper` 技能的独立流程）
- ❌ 不要在巡检报告中包含非问题项的详细描述（保持简洁）

## 搭配使用

- `dead-code-sweeper` — 巡检发现死代码后，触发独立的清理流程
- `regression-guard` — 修复巡检发现的问题后，确保不引入回归
- `doc-sync-check` — 针对文档维度的更轻量级检查
