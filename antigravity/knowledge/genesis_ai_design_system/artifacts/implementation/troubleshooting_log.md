# Troubleshooting Log: Image Extraction and Rendering

This log documents specific, hard-to-track bugs and edge cases encountered during the development of the **Briefing Studio** image extraction and rendering pipeline.

## 1. Mammoth.js Browser-Side Image Failures

### Symptom
Users report that images from a DOCX file are not appearing in the generated briefing, even though the layout contains "image" blocks and the "AI Layer" confirms image placeholder generation.

### Diagnostics
- **Node.js Verification**: Running `mammoth` on the same DOCX in a Node.js environment successfully extracts 7 images (JPEG/PNG).
- **Console Logs**: The log `📷 从 DOCX 提取了 X 张图片` in `GenerationPanel.tsx` may show 0 even when images are present in the file if the extraction logic fails silently.

### Root Causes (Identified)
- **Base64 Stack Overflow & Performance**: Using `String.fromCharCode(...uint8array)` on large images exceeds the call stack limit. Even manual loops are slow for multi-MB images. **Solution**: Use `FileReader.readAsDataURL(new Blob([buf]))` for browser-native performance and safety.
- **Missing Global `Buffer`**: `mammoth.js`'s `image.read()` internal logic assumes a Node.js environment and expects `Buffer`. In browsers, this causes `ReferenceError: Buffer is not defined`. **Solution**: Install the `buffer` polyfill and configure the bundler (Vite) to inject it as a global.
- **Asynchronous Closure**: `extractedImages` state in `App.tsx` being captured by a stale closure in the `handleGenerate` async function. **Solution**: Use `extractedImagesRef` (`useRef` pattern) to ensure the latest state is always accessed across awaits.
- **State Overwrite (Batching)**: Calling `setBriefingData` twice in the same tick (once for API data, once for populated images) caused React to batch and potentially clobber the image-populated update. **Solution**: Merge into a single `finalData` object and perform a single `setBriefingData(finalData)` update.

### Unresolved Edge Case: Browser Environment
If the above fixes are applied and images still fail to appear in the browser:
- **Image Type Compatibility**: Some specialized Word image formats (e.g., EMF, WMF) are not natively supported by browsers or Mammoth's default `imgElement` handler.
- **Memory Limits**: Large Base64-encoded strings (multiple images of several MBs each) can cause UI lag or silent rendering failures in constrained browser environments.
- **Mammoth Browser Version**: Ensure `mammoth.browser.js` is correctly handling the `image.read()` promise-based API which may return `ArrayBuffer` differently than the Node.js `Buffer`.

## 2. Text Scaling Flaws

### Symptom
Text appears truncated despite "auto-font-sizing" logic being active, or Section Headers appear too small relative to body text.

### Findings
- **Horizontal Overflow**: Standard `scrollHeight` checks do not catch horizontal truncation in single-line headers. `scrollWidth` must also be monitored.
- **Unit Propagation**: The `autoFontSize` state must be explicitly passed to inner `<EditableField />` components. If children read `block.style.fontSize` directly, the parent's scaling logic has no visual effect.
- **Scaling Heuristics**: Initializing headers at a fixed 20px is insufficient for large canvas layouts. Using a percentage of the container height (e.g., 40-45%) provides a better visual starting point for the scaling algorithm.
