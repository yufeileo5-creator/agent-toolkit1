# AI Model Configurations

The "指哪生哪图" (Genesis AI Image Design System) supports multiple AI models for image generation and editing.

## Supported Models

### Nano Banana 2 (Gemini 3.1 Flash Image Preview) - **Primary**
- **Model ID**: `gemini-3.1-flash-image-preview`
- **UI Label**: Nano Banana 2 (🍌)
- **Positioning**: The best all-around performance and intelligence-to-cost balance. optimized for speed and high-volume developer use cases.
- **Key Features**:
    - **Flash-Speed Intelligence**: Rapid edits and iterations.
    - **4K Output and Dynamic Aspect Ratios**: Up to 4K resolution and 14 flexible geometries.
    - **Search Grounding**: Incorporation of real-time Google Search and Image Search results.
    - **Subject Consistency**: Tracks up to 5 characters and 14 objects across images.
    - **SynthID Watermark**: All outputs include an invisible, robust watermark for AI safety.

### Gemini 3 Pro (Legacy / Removed)
- **Model ID**: `gemini-3-pro-preview`
- **Status**: Removed from the `AIModel` selection enum in `types.ts` to favor the more efficient Nano Banana 2 model.
- **Description**: Google's previous flagship multimodal model. It was replaced for better performance and cost in the standard workflow.

### OpenAI 5.2 (External/Custom)
- **Model ID**: `openai-5.2-preview` (Placeholder)
- **UI Label**: OpenAI 5.2 (Custom Kernel)
- **Description**: Placeholder for integrating OpenAI-compatible APIs for custom rendering kernels.

## Mapping UI to Service

The `AIModel` enum in `types.ts` maps UI selection to the model identifiers used in `services/geminiService.ts`.

| Feature | Service Function | Model Used |
|---------|------------------|------------|
| Text-to-Image | `generateImage` | `selectedModel` from config |
| Generative Edit | `editImage` | `selectedModel` from config |
| Sketch-to-Image | `generateFromSketch` | `selectedModel` from config |
| Inpainting | `editImage` (masked) | `selectedModel` from config |

## Detailed Capability Guide

For a comprehensive guide on model variants (Pro vs Flash vs 2.5), grounding, consistency, and SDK configuration patterns, refer to:
- [`nanobanana_capabilities.md`](./nanobanana_capabilities.md)
