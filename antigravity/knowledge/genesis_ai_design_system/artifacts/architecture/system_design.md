# Genesis AI Image Design System Architecture

The "指哪生哪图" (Genesis AI Image Design System) is built as a single-page application (SPA) centered around a collaborative design workspace.

## Component Layout

- **`App.tsx`**: Main entry point managing application state (selected tools, AI config, layers, loading states, MCP connections).
- **`Toolbar.tsx`**: Left-side vertical toolbar for selection/modification tools.
- **`CanvasBoard.tsx`**: The core interactive canvas component (renders layers, handles interactions).
- **`PropertyPanel.tsx`**: Right-side dynamic property panel (tool settings, AI prompt input, generation controls).
- **`LayerPanel.tsx`**: Right-side bottom layer list manager.
- **`SettingsModal.tsx`**: Configuration interface for selecting AI models and MCP servers.

## State Management

Application state is primarily managed using React `useState` and `useRef` in the `App.tsx` component, then passed down via props. 
- **Layer System**: Represented as an array of `Layer` objects (`{ id, name, visible, locked, opacity, x, y, fillColor }`).
- **AI Configuration**: Defined by the `AIConfig` interface (`{ aspectRatio, imageSize, selectedModel }`).
- **Task Management**: Uses a `requestIdRef` (incrementing counter) for cancelling outdated AI generation requests.

## AI Services and Operations

The application leverages `geminiService.ts` to interact with Google's Generative AI. 

- **Tool-AI Mapping**:
  - `ToolType.GEN_IMAGE`: Calls `generateImage(prompt, aiConfig)`.
  - `ToolType.GEN_EDIT`: Calls `editImage(compositeImageData, prompt, aiConfig)`.
  - `ToolType.GEN_SKETCH`: Calls `generateFromSketch(compositeImageData, prompt, aiConfig, sketchStrength)`.
  - `ToolType.GEN_INPAINT`: Calls `editImage(maskedImageData, prompt, aiConfig)`.
- **Canvas-AI Interaction**:
  - `CanvasBoard` provides handles for `getCompositeImageData()` (full canvas snapshot) and `getMaskedImageData()` (masked area snapshot).
  - Generation results (base64/data URLs) are loaded back into the active layer or applied to a specific region (inpainting).

## Model Context Protocol (MCP) Integration

- **`mcpService.ts`**: Provides methods `sendToApp` and `getFromApp` to communicate with external MCP servers for additional image processing functionality.
- Supported server types: `image-editor`, etc.
