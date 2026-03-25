# Genesis AI Image Design System (指哪生哪图)

The **Genesis AI Image Design System** (AI 创意工坊 PRO) is a professional-grade AI-assisted image design platform that combines traditional desktop publishing (DTP) paradigms with modern generative AI capabilities.

## Technical Stack

- **Frontend Framework**: React 19 (Vite-based)
- **Styling**: Tailwind CSS
- **Iconography**: Lucide React
- **AI Core**: Google Generative AI (`@google/genai`). High-efficiency image generation powered by **Nano Banana 2** (Gemini 3.1 Flash Image Preview, model ID: `gemini-3.1-flash-image-preview`).
- **Communication**: Model Context Protocol (MCP) for application interaction.

## Key Features

1. **Photoshop-style Interface**:
   - Multi-layer management (visible, locked, opacity, Z-index ordering).
   - Tool-based canvas interaction (Brush, Eraser, Magic Wand, Lasso, Select).
2. **Generative AI Integration**:
   - **Text-to-Image**: Generate images from text prompts.
   - **Generative Edit**: Modify existing image content based on prompts.
   - **Sketch-to-Image**: Transform hand-drawn sketches into polished images with adjustable influence strength.
   - **Generative Inpainting**: Replace or fill specific masked areas using AI.
3. **Professional Controls**:
   - Feathering and Inverting selections.
   - Magic Wand with adjustable tolerance.
   - Support for multiple aspect ratios (1:1, 3:4, 4:3, 16:9, 9:16) and resolutions (1K, 2K, 4K).
4. **Environment Flexibility**:
   - Supports both standalone deployment (via `.env` API keys) and AI Studio integrated environments (via `window.aistudio` authorization).

## Briefing Studio (AI 智能排版)

A specialized module within the system for automated multi-page briefing and document layout generation.
- **Automated Layout**: Uses AI to parse text and images from uploaded DOCX documents and maps them to predefined or AI-suggested layouts.
- **Workflow-Driven Editor**: Features a one-click generation flow, block label controls, and an integrated document content panel.
- **Robust Image Integration**: Automatically extracts images from Word documents using high-performance browser APIs (`FileReader`, `Blob`) and Node.js polyfills (`Buffer`) to ensure stability. See [Briefing Generation Flow](./implementation/briefing_generation_flow.md).
- **Responsive Typography**: Implements a self-correcting font scaling algorithm to prevent text overflow in layout blocks, with support for manual overrides and visual hierarchy preservation. See [Text Rendering Optimizations](./implementation/text_rendering_optimizations.md).

## Critical Implementation Patterns

### React State Management
The system prioritizes consistent state across asynchronous UI interactions.
- **Asynchronous Synchronization**: Uses `useRef` to solve React's stale closure problem in long-running callbacks and timeouts.
- **Defensive Validation**: Employs Zod schemas (`briefingValidator.ts`) to ensure AI-generated content matches expected data structures. See [AI Data Schemas and Validation](./implementation/ai_data_schemas_and_validation.md).
- **Timing Logic**: Implements specific `setTimeout` delays in modal closing sequences to ensure state reconciliation before subsequent async tasks. See [React State Management](./implementation/react_state_management.md).
