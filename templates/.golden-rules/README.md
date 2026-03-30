# .golden-rules/ — 黄金准则目录

> 本目录存放**可执行的质量检查准则**，是 Harness Engineering 中 "Golden Principles" 的落地实现。
>
> 与全局规则（`GEMINI.md`）的区别在于：这些准则是**项目级别**的、**可逐条检查**的、**从历次失败中沉淀**出来的。

## 文件说明

| 文件 | 关注维度 | 检查时机 |
|------|---------|---------|
| `architecture.golden.md` | 分层依赖、模块边界 | 修改 `src/` 下的 import 后 |
| `code-quality.golden.md` | 类型安全、函数长度、防御性 | 每次代码修改后 |
| `documentation.golden.md` | 文档同步、变更日志 | 功能完成标记 `[x]` 后 |
| `error-hints.golden.md` | AGENT_HINT 自修复模板 | Agent 遇到特定错误时 |

## 使用方式

### Agent 自检
Agent 在交付前应逐条对照对应的 `.golden.md` 检查。每条准则格式为：

```
- [GR-XXX] 规则描述
  → 检查方法: 具体的检查步骤
  → 违规信号: 什么情况下算违规
  → 修复方式: 如何修复
```

### harness-gc 巡检
`harness-gc` 技能会定期扫描代码库，用黄金准则作为判定标准。

## 新增准则流程

当 Agent 犯了同样的错误 2 次以上，应该：
1. 分析根因
2. 编码为新的黄金准则条目
3. 追加到对应的 `.golden.md` 文件
4. 更新本 README 的文件说明（如有必要）

> **来源追溯**: 每条准则应标注来源（如 `来源: 第八期长图文开发踩坑`），方便未来评审。
