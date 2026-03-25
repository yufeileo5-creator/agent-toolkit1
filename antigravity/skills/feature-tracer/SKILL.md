---
name: feature-tracer
description: >-
  功能追踪与归档技能。在完成新功能开发后自动触发，将功能与代码实现的映射关系归档到
  docs/feature-map.md 并注入 DSP 图谱标签。也支持通过 /trace 命令按需查询功能对应的代码位置。
  「功能追踪」「feature trace」「代码地图」「功能归档」「/trace」「实现在哪」「哪个文件」等场景触发。
---

# Feature Tracer — 功能追踪技能

将**业务功能/需求**与**代码实现**建立持久映射，解决"这个功能的代码在哪？"的问题。

## 核心机制

双层追踪：
1. **人类层**：`docs/feature-map.md` — 累积记录，Ctrl+F 可搜
2. **AI 层**：DSP 图谱 `features` 标签 — AI 做变更分析时自动感知

## 前置条件

- 项目已初始化 DSP（`.dsp/` 目录存在）
- `docs/feature-map.md` 文件存在（如不存在则首次运行时创建）

## 工作流

### 模式 A：归档模式（功能完成后触发）

**触发时机**：功能开发完成、验证通过后，在生成 walkthrough 之前执行。

#### 步骤 1：收集变更信息

从以下来源提取信息（按优先级）：
1. 当前对话的 `implementation_plan.md`（最权威）
2. `git diff --name-only`（最客观）
3. `walkthrough.md`（如果已生成）

#### 步骤 2：提炼关键文件

从变更文件中筛选出以下类别的关键文件（忽略配置、测试、样式等辅助文件）：

| 类别 | 说明 | 示例 |
|------|------|------|
| **入口组件** | 用户交互的第一个组件/页面 | `XxxPanel.tsx`, `XxxPage.tsx` |
| **核心逻辑** | 业务算法/服务层 | `xxxService.ts`, `xxxEngine.ts` |
| **数据结构** | 类型定义/接口 | `xxx.types.ts`, `xxxSchema.ts` |
| **提示词/模板** | AI 提示词或模板文件 | `xxxPrompt.ts` |
| **状态管理** | Store/Context/Hook | `useXxx.ts`, `xxxStore.ts` |

每个类别最多列 2-3 个最核心的文件，不要贪多。

#### 步骤 3：落地 — 更新 feature-map.md

在 `docs/feature-map.md` 文件的**最顶部**（标题之后）追加一条新记录：

```markdown
---

### 🎨 [功能名称] ([日期 YYYY-MM-DD])
- **入口组件**：[basename](file:///absolute/path) → `ComponentName`
- **核心逻辑**：[basename](file:///absolute/path) → `functionName()`
- **数据结构**：[basename](file:///absolute/path) → `InterfaceName`
- **版本**：vX.X.X（如有）
```

**格式规则**：
- 文件名使用 Markdown 链接 `[basename](file:///path)` 以支持编辑器内点击跳转
- 每个类别只列最关键的 1-3 个文件
- 如果某类别不涉及，直接省略该行
- 新记录追加在文件顶部（最新的在最前面），旧记录自动下沉

#### 步骤 4：落地 — DSP 图谱打标签

使用 `dsp-cli tag-feature` 命令给步骤 2 中筛选出的关键文件对应的 DSP 实体打上功能标签。

```bash
# 先用 find-by-source 找到实体 UID
python <skill-path>/scripts/dsp-cli.py --root <project-root> find-by-source <file-path>

# 再用 tag-feature 打标签（支持多个 UID）
python <skill-path>/scripts/dsp-cli.py --root <project-root> tag-feature "<功能名称>" <uid1> <uid2> ...
```

**注意**：
- 功能名称应简洁一致，如"AI嵌套布局"、"文档解析"
- 如果实体尚未在 DSP 中注册，**跳过打标签**（不要为了打标签而创建大量 DSP 实体）
- 如果 DSP 图谱为空（无实体），跳过此步骤，仅执行步骤 3

---

### 模式 B：查询模式（用户触发 `/trace`）

**触发条件**：用户使用 `/trace` 或提问"XX 功能的代码在哪？"

#### 正向查询：功能名 → 代码

1. 先在 `docs/feature-map.md` 中搜索功能名称
2. 使用 `dsp-cli find-by-feature "<功能名>"` 查找 DSP 图谱中的关联实体
3. 综合两个来源的信息，输出给用户

#### 反向查询：文件名 → 功能

1. 使用 `dsp-cli find-by-source <path>` 找到实体
2. 读取实体的 `features` 字段
3. 在 `docs/feature-map.md` 中搜索相关功能的完整记录
4. 输出该文件参与了哪些功能

---

## DSP CLI 命令参考

```
# 给实体打功能标签（支持多个 UID）
dsp-cli tag-feature <feature-name> <uid1> [<uid2> ...]

# 移除实体上的功能标签
dsp-cli untag-feature <uid> <feature-name>

# 列出所有已注册的功能标签
dsp-cli list-features

# 按功能标签查找关联实体
dsp-cli find-by-feature <feature-name>

# 搜索（已支持 features 字段）
dsp-cli search <query>
```

## 常见反模式

- ❌ **记录太多文件**：只记核心文件，不要把每个改动的文件都列上去
- ❌ **功能名称不一致**：同一功能在不同地方用不同名称（如"嵌套布局" vs "嵌套容器"）
- ❌ **遗漏 DSP 标签**：只更新了文档但忘记打 DSP 标签
- ❌ **把 bug fix 和新功能混在一起**：小修复不需要归档到 feature-map，除非是重大修复
- ✅ **功能名称保持稳定**：一旦确定就不要改，其他地方引用时使用完全相同的名称
