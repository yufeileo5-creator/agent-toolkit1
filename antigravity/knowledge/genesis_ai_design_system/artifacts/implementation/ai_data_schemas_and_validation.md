# AI Data Schemas and Validation

The **Briefing Studio** relies on a strict data validation layer to handle the inherently unstable nature of AI-generated JSON responses. This layer ensures that even if the AI omits fields or returns incorrect types, the rendering engine receives a safe, typed object.

## Core Validation Architecture

The system uses **Zod** for runtime validation and **Immer** for immutable updates. The validation logic is centralized in `src/domain/validators/briefingValidator.ts`.

### Block-Level Schemas

Every layout block has a corresponding Zod schema that implements defensive transformations:

| Block Type | Expected Data Structure | Fallback Strategy |
|------------|------------------------|-------------------|
| `title` | `{ content: string }` | Defaults to "无标题" |
| `text` | `{ paragraphs: string[] }` | Converts string to array; defaults to ["暂无内容"] |
| `image` | `{ url: string }` | Defaults to empty string (user must upload) |
| `section-header` | `{ content: string }` | Generated title; defaults to "小标题" |
| `card` | `{ title: string, description?: string }` | Defaults to empty title/desc |
| `quote` | `{ content: string, author?: string }` | Defaults to "暂无引言" |
| `list` | `{ items: Array<{ title, description }> }` | Defaults to placeholder items |
| `cta` | `{ content: string }` | Generated CTA text; defaults to "了解更多" |

### Defensive Prompting (The Schema-Prompt Link)

The `GeminiClient` and `OpenAIClient` generate a JSON Schema from the layout template blocks before calling the API. 

**Blocking Logic**: For `image` and `line` blocks, the prompt explicitly instructs the AI to return an empty string or omit content (as these are handled by doc extraction or are purely visual). For `section-header`, `card`, and `cta` blocks, explicit schema descriptions ensure the AI generates contextual content (e.g., "brief section summary" for headers) rather than just static placeholders.

The schema generated for the API is mirrored in the Zod validator.

**Key Design Pattern**: The ID of the `LayoutBlock` is used as the key in the AI's JSON response.

```typescript
// AI Response Structure (BriefingData)
{
  "blocks": {
    "t1": { "type": "title", "content": "AI Design Revolution" },
    "ib1": { "type": "image", "url": "" },
    "sh1": { "type": "section-header", "content": "Process Overview" }
  },
  "metadata": { ... }
}
```

## Parsing and Sanitization Logic

The `parseAIPayload` function in `briefingValidator.ts` handles the mapping:

1. **Iteration**: Loops through all block IDs defined in the layout template.
2. **Missing Blocks**: If a block ID is missing from the AI response, `createDefaultBlockData` is invoked to provide a safe placeholder.
3. **Type Coercion**: Uses Zod `.transform()` or `.catch()` to fix common AI errors (e.g., providing a string for an array field).
4. **Data Path Normalization**: AI responses are often flattened. The validator ensures the hierarchy `{ blocks: { [id]: data } }` is maintained.

## Data Interoperability with Images

When DocX images are extracted, they are injected into the *already validated* BriefingData structure. To avoid corruption:
- Sub-object targeting: Updates must target `data.blocks[blockId].url`.
- Deep Cloning: Uses `JSON.parse(JSON.stringify(response.data))` before modification to break references and ensure the store receives a clean update.

## Common Pitfalls: Adding New Block Types

When introducing a new block type (e.g., `card`, `cta`), the following three areas **must** be updated simultaneously:

1.  **Validator (`briefingValidator.ts`)**: Add the Zod schema and include it in `BlockDataSchema` union. Update `createDefaultBlockData` and `parseAIPayload` switch cases.
2.  **API Client (`GeminiClient.ts`)**: Add the type to `buildSchemaProperties` (for the prompt schema) and update the default value handling in `generateBriefingData`.
3.  **UI Components**: Ensure the renderer (e.g., `BriefingCanvas.tsx`) has a mapping for the new type to a React component.

**The "Text Fallback" Bug**: If a type is added to the layout but omitted from the `GeminiClient` or `briefingValidator` switch cases, it often falls back to a generic `text` type or returns an empty object, causing runtime rendering errors or missing content.
