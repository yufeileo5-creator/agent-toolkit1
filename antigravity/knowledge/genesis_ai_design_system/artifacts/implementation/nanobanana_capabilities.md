# Nano Banana (Gemini Image) Capabilities and Guide

The "Nano Banana" series represents Google's Gemini-family models optimized for image generation and editing using the Generative AI (Imagen) technology.

## Model Variants

| Model Name | Internal ID | Performance Profile | Key Use Cases |
|------------|-------------|---------------------|---------------|
| **Nano Banana Pro** | `gemini-3-pro-image-preview` | Professional production, high-fidelity, complex prompts. | 4K assets, complex multi-step instructions, grounding with Search. |
| **Nano Banana 2** | `gemini-3.1-flash-image-preview` | Best overall balance of intelligence, speed, and cost. | Standard high-quality generation, rapid edits, high-volume production. |
| **Nano Banana** | `gemini-2.5-flash-image` | High-speed, high-volume, low-latency. | Rapid iterations, 1024px images, budget-constrained tasks. |

## Advanced Features (3.x Series)

### 1. Model Grounding
- **Google Search Grounding**: Leverages real-time web knowledge to generate facutally accurate visual representations of objects, public figures, or current events.
- **Google Image Search Grounding** (3.1 Flash): Uses visual references from the web to guide generation (e.g., specific products or brand assets).

### 2. Multi-Character Consistency
- **Character Consistency**: Maintains the visual identity of up to 5 individual characters across a series of generated images.
- **Object Consistency**: Can track up to 14 specific objects, keeping shapes and textures consistent across scenes.

### 3. Subject-Aware Image Editing
- **Interactive Editing**: Modify backgrounds, swap colors, adjust lighting, or replace foreground elements using natural language instructions.
- **Reference-Guided Editing**: Use up to 14 reference images (for 3.x series) to define styles, characters, or specific structural constraints.

### 4. Text and Composition
- **Stylized Text In-Image**: Enhanced capability to render legible text in multiple languages and styles into the image geometry and textures.
- **Aspect Ratio Adherence**: Precise control over output geometry (up to 14 aspect ratios supported, including extremes like 1:8 or 8:1).
- **Thinking Process** (Pro only): Performs internal reasoning steps to plan complex compositions before initiating the pixel generation phase.

### 5. Watermarking
- **SynthID Digital Watermark**: All images generated or edited via the Gemini 3 series contain an invisible, robust digital watermark as an AI safety measure.

## SDK Configuration Patterns (JavaScript)

When using the `@google/genai` library, use the following configuration structure for optimal results:

```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: API_KEY });

// Standard Generation
const response = await ai.models.generateContent({
  model: "gemini-3.1-flash-image-preview",
  contents: { 
    parts: [{ text: "A futuristic cityscape with nano bananas" }] 
  },
  config: {
    responseModalities: ['Image'], // Returns only the image part
    imageConfig: {
      aspectRatio: "16:9",
      imageSize: "2K" // Options: 1K, 2K, 4K (Model dependent)
    }
  }
});

// Image Editing (Inpainting / Modifying)
const editResponse = await ai.models.generateContent({
  model: "gemini-3.1-flash-image-preview",
  contents: {
    parts: [
      { text: "Change the background to a sunset" },
      { 
        inlineData: { 
          mimeType: "image/png", 
          data: base64ImageData 
        } 
      }
    ]
  },
  config: {
    responseModalities: ['Image']
  }
});
```
