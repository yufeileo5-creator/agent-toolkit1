---
description: >-
  排版引擎核心文件变更时的检查清单
---

# 排版引擎变更检查

当你修改以下任何"受保护文件"时，必须执行此工作流中的检查步骤。

## 受保护文件列表

| 文件 | 核心职责 |
|------|---------|
| `src/App.tsx` | `handleGenerate` 中的图片填充逻辑 |
| `src/services/aiLayoutService.ts` | 骨架生成 + P0-2 图片补偿 |
| `src/infrastructure/api/gemini/GeminiClient.ts` | Stage 2 schema 构建 + prompt |
| `src/domain/validators/briefingValidator.ts` | AI 数据验证 + 转换 |
| `src/features/briefing/components/BriefingCanvas.tsx` | 画布渲染 |
| `src/features/briefing/components/blocks/ImageBlock.tsx` | 图片显示 |

## 检查步骤

// turbo-all

### 1. 运行契约测试
```bash
npm test
```
确认所有测试通过，无新增失败。

### 2. 类型检查
```bash
npm run lint
```

### 3. 核心契约审查

修改前请确认以下契约不被破坏：

- **P0-1 无条件填充**：`App.tsx` 中图片填充不受 `if` 条件守卫
- **P0-2 补偿保证**：`aiLayoutService.ts` 中 `deficit > 0` 时追加 image block
- **P0-3 独立约束**：`aiLayoutService.ts` 中 prompt 的 image 数量独立于 text block 数量
- **P1-4 尺寸感知**：`GeminiClient.ts` 中 text block description 包含 `占画布约 X%`
- **P1-5 截断**：`GeminiClient.ts` 中文本超 6000 字时截断并标注

### 4. 浏览器验证（如有重大改动）

上传 `简报.docx` 测试：
- Bug A：画布中 image 区块数 ≥ 文档图片数
- Bug B：图片可见（非空白占位符）
- Bug C：文字填满其矩形区域
