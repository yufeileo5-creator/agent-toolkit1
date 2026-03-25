# AI Layout System Design

The Genesis system separates **Layout Generation** (structural arrangement) from **Content Generation** (data population). This decoupling allows for more stable and predictable results.

## Decoupling Strategy

### 1. Structural Layout (AILayoutService)
- **Goal**: Decide where blocks are placed (x, y, w, h) and what types they are.
- **Input**: User text + Style preference (e.g., "News", "Magazine").
- **Output**: An array of `LayoutBlock` objects.
- **AI Logic**: The style description is injected into the prompt as a creative suggestion ("News style likes bold headers and hero images"). The response schema ensures coordinates are valid percentages (0-100).

### 2. Content Generation (GeminiClient)
- **Goal**: Populate the specific blocks with meaningful content derived from the document.
- **Input**: User text + The finalized layout blocks from the previous step.
- **Output**: A `BriefingData` object with a `blocks` map where keys match the layout block IDs.
- **AI Logic**: Strict JSON Schema enforcement. Each block ID in the layout becomes a property in the AI's output.

## Technical Implementation Details

### Coordinate System
- **Relative Units**: All blocks use percentage-based coordinates (`x`, `y`, `w`, `h` from 0-100).
- **Transformation**: The frontend maps these percentages to actual pixel values based on the `canvasSize` (e.g., 800x1200).

### Schema Injection
When calling the content generation API, the system dynamically builds a JSON Schema based on the *currently active layout blocks*.
- **Selective Prompting**: Some blocks (like `image`) are marked with "Return an empty string" descriptions in the schema because their content is supplied by the frontend's document extraction logic, not by the LLM.
- **Recursive Parsing**: Blocks like `list` and `card` have nested object schemas to ensure structured data (e.g., arrays of objects with `title` and `description`).

### post-AI Processing (Post-Correction)
After the AI returns a layout or content:
1. **Safety Clamping**: Coordinates are clamped to [0, 95] to prevent overflow.
2. **Dimension Correction**: Ensures `x + w <= 100` and `y + h <= 100`.
3. **ID Generation**: Assigns stable, type-prefixed IDs (e.g., `ai_text_17730...`) for React rendering.
