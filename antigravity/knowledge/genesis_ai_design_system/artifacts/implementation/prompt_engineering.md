# Briefing System Prompt Engineering

The **Briefing Studio** relies on two distinct AI generation phases: **Layout Generation** (structural blueprint) and **Content Extraction** (populating the blueprint). Both require precisely engineered prompts to ensure professional results.

## 1. AI Layout Prompt Rules (`AILayoutService.ts`)

The AI acts as a "Professional Graphic Designer" to output a JSON array of `LayoutBlock` objects.

### Visual Hierarchy & Dimension Constraints
- **Title Block**: Must be at the top, `80-100%` width, `6-10%` height.
- **Text Blocks**: Minimum `45%` width, at least `15%` height to ensure readability and prevent excessive font shrinking.
- **Section Headers**: `40-60%` width, `4-6%` height.
- **Image Blocks**: Must have at least `20%` height to provide impact.
- **Quotes**: `60-80%` width for visual break.

### Spacing & Layout Logic
- **Constraint**: **3% minimum padding/margin** between all blocks (enforced by instructions like *"Blocks must not overlap and should have comfortable spacing"*).
- **Coordinate System**: 0-100 percentage-based grid.
- **Grouping**: Instructions to favor side-by-side layouts (e.g., Image next to Text) for visual richness.

### Image Count Enforcement
- **Crucial Rule**: To prevent "empty image block" or "nowhere to put images" bugs, the prompt is injected with a mandatory image count:
  > *"Source document contains N images; you MUST generate exactly N blocks of type 'image' to accommodate them."*

---

## 2. Content Extraction Prompt Rules (`GeminiClient.ts`)

The AI act as a "Professional Briefing Copywriter" to populate specific block IDs mapped to the layout.

### Substance Enforcement
- **Primary Instruction**: Every text block **must have substantial content**. AI is forbidden from returning empty strings or small placeholders.
- **Summarization Pattern**: Instead of raw extraction, AI is told to *"Extract and polish relevant paragraphs from the source text"*.
- **ID-to-Role Mapping**:
    - `text`: Returns a string array (paragraphs).
    - `section-header`: Must be a context-bound title (e.g., "Project Milestones") rather than the technical name "Small Title".
    - `quote`: Must be a powerful "Golden Quote" or core insight from the text.
    - `footer`: Standard operational or metadata footer.

### Preventing Content Duplication

When multiple blocks of the same type (e.g., `text`, `card`) exist, AI may inadvertently generate similar content for all of them if the schema descriptions are identical.

-   **Description Variation**: The dynamic JSON schema should include the block ID in the description (e.g., `"Content for block: [ID]"`) to force the LLM to treat them as distinct entities.
-   **Contextual Role Assignment**: In the prompt, the AI is instructed to divide the document's narrative flow across the available text blocks in sequence, rather than summarizing the whole document into each block.

---

## 3. Formatting and Structure

Both prompts use **JSON Output Mode** with explicit TypeScript-like schemas passed in the `responseSchema` configuration of the SDK. This ensures that the frontend can reliably parse coordinates and nested data structures (like paragraph arrays or data tables).
