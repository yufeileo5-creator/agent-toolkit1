# Briefing Generation Workflow

The **Briefing Studio** feature provides a seamless workflow from document upload to AI-powered layout and content generation.

## User Interface Enhancements

### Layout Editor Modal Features
- **One-Click "Generate Briefing"**: A dedicated button (Play icon) in the bottom toolbar that saves the current layout, closes the editor, and triggers the main generation process with a 200ms delay to allow UI reconciliation.
- **Block Label Toggle**: An Eye/EyeOff toggle in the toolbar allows users to hide/show block labels on the canvas to preview the layout cleanly.
- **Document Content Panel**: A collapsible left-sidebar panel that shows the extracted text in a `textarea`. Users can edit the source content or re-upload documents directly within the layout editor.

### Template Preview Logic
In the main sidebar's template list, blocks are rendered as wireframes. To maintain visual clarity:
- **Simplified Content**: Instead of showing high-level labels (which can be long and clutter the thumbnail), the `WireframeBlock` component displays the block's technical type name (e.g., "标题", "图片", "正文", "引言").


## Document Processing Pipeline

### DOCX Extraction
The system uses `mammoth.convertToHtml` with a custom `images` handler to extract both text and embedded images from Word documents.
- **Efficient Base64 Conversion**: Direct Base64 conversion via `btoa(String.fromCharCode(...))` is avoided for large images to prevent stack overflow errors. The system uses the **`FileReader.readAsDataURL(Blob)`** API for efficient, browser-native conversion.
- **Node.js Dependency Polyfill**: `mammoth.js` internal image reading relies on the Node.js `Buffer` object. In a Vite/Browser environment, this causes `ReferenceError: Buffer is not defined`.
    - **Fix 1 (Vite Config)**: Set `'global': 'globalThis'` in `define` and add `'buffer': 'buffer/'` in `resolve.alias`.
    - **Fix 2 (Entry Point)**: In `main.tsx`, `import { Buffer } from 'buffer';` and set `(window as any).Buffer = Buffer;`.
- **Images**: Converted to Base64 Data URLs and stored in the `extractedImages` state array.
- **Text**: Extracted as raw text for AI processing.

### Image-to-Block Mapping
After AI generates the briefing content, the system automatically fills `image` type blocks with the images extracted from the document.
- **Data Path**: The fill logic target is `updatedData.blocks[blockId].url`.
- **Logic**: Images are filled in the order they appear in the document into the available image blocks in the layout.

```typescript
// Core mapping logic in App.tsx
if (extractedImages.length > 0 && response.data?.blocks) {
  const imageBlocks = currentTemplate.blocks.filter(b => b.type === 'image');
  // ... check if imageBlocks count matches extractedImages count
  // mapping happens here...
}
```

### AI-Driven Image Placeholder Enforcement
To ensure documentation images are correctly placed, the **AI Layout Service** must be aware of the number of extracted images.
- **Enforcement Logic**: The `imageCount` is passed to the `generateAILayout` request.
- **Hard Constraint**: The prompt includes a mandatory instruction: *"Source document contains N images; you MUST generate exactly N blocks of type 'image' to accommodate them."* (See [Prompt Engineering](./prompt_engineering.md) for details).
- **Benefit**: This prevents the AI from choosing an image-less layout for a document that clearly requires visual placeholders.

> [!IMPORTANT]
> **Multi-Entry Consistency**: The image filling logic must be applied at every briefing generation entry point. A common bug occurs when logic is added to the "Final Generate" button but omitted from the "AI Layout Preview" flow, leading to empty image areas when users generate layouts from within the editor panel.

## AI Content Validation

The `briefingValidator.ts` uses Zod to ensure AI responses conform to the schema for various block types.
- **New Supported Types**: `section-header`, `card`, `cta`.
- **Defensive Defaults**: Each type has a fallback (e.g., `section-header` defaults to "小标题", `cta` defaults to "了解更多") to prevent rendering errors if the AI omits a block.

## User Experience Design

### Conditional Editor Activation
The system distinguishes between document processing and AI layout generation via an `openEditor` flag in the `onAutoLayout` callback:
- **Document Upload**: Updates the template blocks based on the document structure (`onAutoLayout(blocks, false)`) but *does not* automatically open the layout editor modal.
- **AI Layout Generation**: Triggered from the "Briefing Styles" section. Upon successful completion (`onAutoLayout(blocks, true)`), it both updates the template and *automatically* opens the layout editor to let users review the AI's work.


### Visual Feedback
During the generation process, a prominent loading overlay is applied to the briefing canvas:
- **Full-Screen Mask**: A `white/80` or `zinc-900/80` backdrop with a blur effect.
- **Animated Indicator**: A large spinning circle with a pulse effect and high-priority z-index (`z-50`).
- **Status Messages**: Clear text indicating the current AI task (e.g., "AI 正在生成简报...").
### Performance and Availability
- **API Generation Limits**: Content generation with complex layouts and detailed substance enforcement requires significant LLM processing time. To avoid premature failures, **client-side timeouts have been removed**, allowing the system to wait until the AI naturally completes or the provider returns a standard error. This ensures complex briefings are generated fully without interruption.
- **Service Integration**: The `AILayoutService` and `GeminiClient` are unified under a common `createGeminiClient` factory to handle configuration consistently (e.g., standardizing the experimental `gemini-3-flash-preview` model version).
- **Image Count Synchronization**: The layout generation phase is explicitly passed the `extractedImages.length`. This ensures the AI selects a layout that matches the physical image count of the document, preventing data-view mismatches.
