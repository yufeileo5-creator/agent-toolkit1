# 🤖 Agent Toolkit

> AI Agent 的全局配置、技能和工作流集合，基于 OpenAI Harness Engineering 范式构建。

## 目录结构

```
.gemini/
├── GEMINI.md                        # 全局代理规则（9 章节）
├── _versions/                       # 历史版本归档
├── antigravity/
│   ├── skills/                      # 技能库（93 个技能目录）
│   │   ├── harness-gc/              # Harness 垃圾回收巡检
│   │   ├── agent-eval/              # Agent 质量评估
│   │   ├── pua/                     # 反摆烂引擎（+失败沉淀闭环）
│   │   ├── sdd-plan/                # 规格驱动开发
│   │   ├── systematic-debugging/    # 系统化调试
│   │   ├── code-review/             # 代码审查
│   │   ├── regression-guard/        # 回归守卫
│   │   ├── plugin-dev/              # 插件开发指南
│   │   ├── pm-*/                    # 产品管理技能（50+）
│   │   └── ...                      # 更多技能
│   └── global_workflows/            # 全局工作流
│       ├── doc-sync-check.md        # 文档同步检查
│       ├── handoff.md               # 上下文交接
│       ├── plan.md                  # 计划模式
│       ├── version.md               # 版本管理
│       └── layout-engine-check.md   # 排版引擎检查
```

## 快速开始

1. 将本仓库克隆到 `~/.gemini/` 目录（或你的 Agent 配置目录）
2. `GEMINI.md` 将被 Agent 自动加载为全局规则
3. `skills/` 中的技能按需触发
4. `global_workflows/` 中的工作流通过 `/` 命令触发

## 设计理念

基于 **OpenAI Harness Engineering** 的六大核心组件：

| 组件 | 实现方式 |
|------|---------|
| Context Engineering | GEMINI.md + 渐进式规则路由 |
| Architectural Constraints | 分层依赖规则 + DSP 图谱 |
| Garbage Collection | harness-gc 技能 |
| Agent Loop | sdd:plan → 实现 → verification |
| Tool Integration | MCP + 插件注册表 |
| Evaluation | agent-eval 技能 |
| Sandbox Security | 文件操作边界规则 |

## 技能分类

| 类别 | 数量 | 代表技能 |
|------|------|---------|
| 🏗️ 架构 & 工程 | ~15 | harness-gc, regression-guard, plugin-dev |
| 🧪 质量 & 测试 | ~8 | agent-eval, code-review, test-driven-development |
| 🎨 前端 & 设计 | ~5 | baseline-ui, taste-skill, canvas-design |
| 📝 文档 & 交付 | ~5 | docs-writer, docs-changelog, pr-creator |
| 📊 产品管理 | ~50 | 竞品分析, 用户画像, 定价策略, GTM等 |
| 🛠️ 调试 & 修复 | ~5 | systematic-debugging, pua, feasibility-check |

## 许可

私有配置仓库，仅供个人使用。
