---
name: long-form-content
description: >-
  当用户或 API 提供非结构化的营销文案（Word、Excel）并要求生成或排版"长图"、"长图文"、"活动海报"或"营销落地页"时触发。该技能将源数据解构并最终产出符合系统规范的、完全可编辑的 Canvas .pen 排版 JSON 布局数据。
---

# 长图文生成 (Long Form Content Generation)

将原生的业务数据（如活动文案的 Word、选品与价格表格 Excel）转换为高品质的、可 100% 被解析并二次修改的 `.pen` 画布节点数据模型。

**核心架构**：Claude / Agent 只输出紧凑的约定格式 Markdown → 由本地 `LongFormMarkdownStrategy` 确定性脚本转为 `.pen` DSL JSON。**严禁直接输出 JSON**。

## Prerequisites
- 提供的 `.docx` 或 `.xlsx` 源文件，或用户通过 API Payload 直接传入的纯文本。
- 当前项目（AI Visual Editor）所支持的 Canvas Engine `.pen` Schema 规则认知。
- 本地已实现的 `LongFormMarkdownStrategy` 解析器（路径：`src/plugins/ai-generate/long-form-strategy.ts`）。

## Workflow / 核心工作流

### Phase 1: Input Extraction (输入提取)
- **动作**：
  - **应用内路径**：前端上传文件到 BFF `POST /api/document/parse`，获取结构化 `{ sections, products, rawRows }`。
  - **Agent Skill 路径**：通过 `run_command` 调用 mammoth/xlsx 解析源文件。
- **关键要求 [★文档完整性保障]**：
  - ⚠️ **严禁概括或省略原始文档的任何实质内容**：每一个商品名、每一条规则、每一个价格、每一个有效期限都必须原封不动地出现在最终输出中。
  - 必须逐行校验：提取文本后，与源文件做交叉比对，确认没有遗漏的行、被合并的条目或被"概括"的段落。
  - 对于 Excel 表格，每一行数据都必须独立映射为一个商品/权益条目，**禁止用"等N项"进行汇总**。

### Phase 2: Design System Token Selection (设计系统匹配)
- **动作**：确定本次长图文使用的设计令牌。
- **Token 格式**（必须与系统保持一致）：
  - 颜色：`$primary.base`、`$secondary.500`、`$neutral.200`（**不是** `$color-primary`）
  - 字体：使用系统支持的高品质字体如 `Plus Jakarta Sans`、`Inter`
  - 间距：`gap: 16`、`padding: 24` 等

### Phase 3: Markdown Generation (输出约定格式 Markdown) [★核心]
- **动作**：将文档内容按约定语法输出为紧凑 Markdown。

**约定语法表**：

| 语法 | 含义 | 转换结果 |
|------|------|----------|
| `# 大标题` | Hero 区活动主标题 | 大字 frame（fontSize:36, fontWeight:900） |
| `## 小标题` | 区块标题 | 中字标题（fontSize:22, fontWeight:700） |
| `> 引用文字` | 活动副标题/宣传语 | 带背景的引用容器 |
| `![描述](placeholder)` | 图片占位 | 灰色占位 frame，中间显示 alt 描述 |
| `---product` | 进入商品列表模式 | 后续 `🏷️` 行收集为商品卡片组 |
| `🏷️ 名称 \| ¥价格 \| ~~¥原价~~ \| 权益` | 单条商品 | 商品卡片（图片占位+名称+价格） |
| `---rules` | 进入规则/条款区 | 后续 `*` 行转为细则文本 |
| `* 规则文本` | 单条规则 | 小字弱色文本（fontSize:11） |
| `[rect WxH $token]` | 装饰矩形 | 带 token 颜色的矩形节点 |
| `普通文本` | 正文段落 | 正文文本节点 |

**文档完整性检查清单**：
- [ ] 源文档中的**每一个商品**都在 `🏷️` 行中有对应输出
- [ ] 所有**价格信息**（现价、原价、总价值）都已精确标注
- [ ] 所有**权益/赠品/优惠券**内容都未被省略
- [ ] 所有**附加条件**（有效期、使用限制、地区限制）都出现在 `---rules` 区域
- [ ] 标题、副标题与源文档一字不差

### Phase 4: Local Conversion (本地脚本转换)
- **动作**：将 Phase 3 输出的 Markdown 喂给 `LongFormMarkdownStrategy.parse(markdown)`，获得标准 `.pen` DSL JSON。
- **规则**：
  - 转换是**纯确定性的**（无 AI 参与），不会产生幻觉。
  - 输出的 DSL 使用 Flexbox 布局（`layout: "vertical"`、`gap`、`padding`），**绝对禁止绝对坐标**。
  - 所有颜色引用 Phase 2 确定的 Token（如 `$primary.base`）。

### Phase 5: Verification & Delivery (验证交接)
- **动作**：
  1. 验证 DSL JSON 结构合法性（顶层 `{ children: [...] }`）。
  2. **回溯校验**：将 DSL 中的文本节点内容与源文档逐项比对，确认零遗漏。
  3. 交付给 Canvas Engine 渲染为可编辑画布。

## Best Practices
- ✅ **内容为王**：文档中的每一个字、每一个价格都必须出现在最终画布上，不允许AI自作主张地"精简"或"概括"。
- ✅ **Markdown 优先**：永远先输出 Markdown 再转 JSON，不要尝试直接生成 .pen JSON（token 消耗大、容易出错）。
- ✅ **占位而非生成**：图片位置只放占位描述（`![描述](placeholder)`），用户后续手动上传或 AI 生成。

## Common Pitfalls
- ❌ **省略商品条目**：Excel 有 15 个商品却只输出了 5 个"代表性"商品 → 必须全部输出。
- ❌ **概括规则条款**：把 8 条细则"概括"成"详见活动规则" → 必须逐条罗列。
- ❌ **直接输出 JSON**：跳过 Markdown 直接生成 .pen JSON → 严禁，必须走 Markdown→脚本转换管线。
- ❌ **硬编码颜色**：写 `#FF2600` 而不是 `$primary.base` → 必须使用 Token 引用。
