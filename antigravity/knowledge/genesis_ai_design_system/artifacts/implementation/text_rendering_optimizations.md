# Text Rendering Optimizations

To handle varied content lengths within the fixed-dimension blocks of the briefing layout, the system implements several rendering optimizations.

## Auto-Font-Sizing (Font Scaling)

The `TextBlock` and `SectionHeaderBlock` components feature a self-correcting font size mechanism to prevent text overflow. This ensures that generated content remains visible even if the AI provides more text than the block's initial dimensions allow.

### Implementation Logic
The system uses a `useEffect` hook that monitors the block's content, dimensions, and base font size.

1. **Measurement**: It compares the `scrollHeight` of the text container against its `clientHeight`.
2. **Adjustment**: If an overflow is detected (`scrollHeight > clientHeight + 2`), the font size is iteratively decreased by 1px.
3. **Constraints**: The scaling continues until the content fits or a minimum font size (e.g., 10px) is reached.
4. **Trigger**: The check re-runs whenever paragraphs change, the block is resized (`w`, `h`), or the base `fontSize` style is modified.

```tsx
// Pattern used in TextBlock.tsx
const hasInitializedRef = useRef(false);
const [autoFontSize, setAutoFontSize] = useState<number>(block.style?.fontSize || 16);

// 1. Initial/Auto Scaling: Runs on content/size changes
useEffect(() => {
  // If user has already manually adjusted (or first fitting done), skip auto-scaling
  if (hasInitializedRef.current && block.style?.fontSize) {
    setAutoFontSize(block.style.fontSize);
    return;
  }
  
  const el = containerRef.current;
  if (!el) return;
  
  let size = block.style?.fontSize || 16;
  el.style.fontSize = `${size}px`;
  
  while (el.scrollHeight > el.clientHeight + 2 && size > 10) {
    size -= 1;
    el.style.fontSize = `${size}px`;
  }
  setAutoFontSize(size);
  hasInitializedRef.current = true;
}, [data.paragraphs, block.w, block.h]);

// 2. Manual Override Sync: Explicitly follow user-tweaked font sizes
useEffect(() => {
  if (hasInitializedRef.current && block.style?.fontSize) {
    setAutoFontSize(block.style.fontSize);
  }
}, [block.style?.fontSize]);
```

### Application in Section Headers
`SectionHeaderBlock` uses an identical pattern but monitors `data.content` instead of paragraphs. 
- **Vertical & Horizontal Check**: Unlike body text which wraps, headers must check both `scrollHeight` and `scrollWidth` to prevent truncation of long titles in narrow blocks.
- **Dynamic Base Size Heuristic**: To ensure titles remain prominent, the base font size is initialized as `Math.max(block.style?.fontSize, clientHeight * 0.45)`. This prevents titles from appearing too small in tall layout blocks.
- **Visual Hierarchy Check**: To prevent titles from becoming smaller than body text, the starting `baseFontSize` for headers should always be at least 2-4px larger than the `baseFontSize` of adjacent `text` blocks.
-   **Vertical & Horizontal Check**: Unlike body text which wraps, headers must check both `scrollHeight` and `scrollWidth` to prevent truncation of long titles in narrow blocks.
-   **Dynamic Base Size Heuristic**: To ensure titles remain prominent, the base font size is initialized as `Math.max(block.style?.fontSize, clientHeight * 0.45)`. This prevents titles from appearing too small in tall layout blocks.
-   **Visual Hierarchy Check**: To prevent titles from becoming smaller than body text, the starting `baseFontSize` for headers should always be at least 2-4px larger than the `baseFontSize` of adjacent `text` blocks.

## The Propagation Trap

A common implementation error discovered was that while the parent block (e.g., `TextBlock.tsx`) calculated the `autoFontSize` correctly, its internal editable fields (e.g., `<EditableField />`) were still reading the static `block.style.fontSize`.

**Fix**: Ensure calculated `autoFontSize` is explicitly passed down to child-level styles to override the template's static values.
 
## Preventing Jitter on Manual Scaling

A "shimmering" or "bouncing" effect occurs when the manual font adjustment logic in the toolbar is coupled too tightly with the auto-font-sizing `useEffect`.

-   **The Problem**: Manual increase → `block.style.fontSize` update → `useEffect` (on `fontSize` change) → detect "overflow" caused by the new size → scale back down to fit → `autoFontSize` goes back to original. Result: Font size cannot be manually increased.
-   **The Solution**: Segregate **Initial Fitting** from **Manual Style Changes**. Use a `ref` (e.g., `hasInitializedRef`) to mark the first fitting completion. Once initialized, the auto-fitting effect only runs if the content (`data.paragraphs`) or block dimensions (`w`, `h`) change, while any manual `fontSize` change is directly accepted by a secondary "manual sync" effect without re-triggering the scaling loop.


## Component-Specific Styling

### Section Header Design Evolution
Originally, `section-header` blocks featured a solid purple background and white text. To improve document homogeneity and support varied themes:
-   **Transparent Background**: Defaulted to `transparent` or light UI grays.
-   **High-Contrast Text**: Specialized to use dark slate colors (`#1e293b`) by default.
-   **Flexible Ordering**: Support for `sectionNumber` display that automatically adapts its accent color based on the presence of a background color.

## Responsive Typography

- **Unit Handling**: Font sizes are defined in pixels but are scaled based on the relative width/height of the canvas blocks.
- **Line Height & Letter Spacing**: These are controlled via the `block.style` object, allowing AI templates to dictate the typographic rhythm.
- **Text Wrapping**: Supports `shape-outside` and CSS floats to wrap text around overlapping image blocks, creating a magazine-style aesthetic.
