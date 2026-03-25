# Layout System and Coordinate Mapping

The design system uses a percentage-based coordinate system for its block-based layout. This ensures that the design remains responsive and consistent across various canvas resolutions and zoom levels.

## Coordinate Mapping Logic

Individual blocks (layers or layout blocks) define their geometry using 0-100% values:
- `x`, `y`: Position of the top-left corner relative to the canvas origin.
- `w`, `h`: Width and Height relative to the canvas dimensions.

### Pixel Calculation
In the rendering engine and export services, these percentages are mapped to fixed pixel dimensions based on the `canvasSize` (e.g., 1K, 2K, 4K).

```typescript
// Example coordinate transformation
const pixelX = (block.x / 100) * canvasSize.width;
const pixelY = (block.y / 100) * canvasSize.height;
const pixelW = (block.w / 100) * canvasSize.width;
const pixelH = (block.h / 100) * canvasSize.height;
```

## Legacy Margin System
Earlier versions of the layout engine included a margin subtraction logic where blocks were contained within a "safe zone" defined by margins. 
- **Current Status**: Deprecated and Removed. 
- All blocks now map directly to the full dimensions of the canvas. For historical details, see the [Margin Removal Analysis](../implementation/margin_removal.md).
