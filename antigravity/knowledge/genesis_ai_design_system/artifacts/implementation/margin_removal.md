# Canvas Margin Feature Removal

The canvas margin feature provided a "safe zone" for content by compressing the active artboard area. While it offered visual consistency, it complicated coordinate calculations and was ultimately removed to streamline the layout engine.

## Historically Affected Components

### 1. State Management
- ** margins** object in the global state (previously `BriefingState` in Zustand).
- `setMargins` actions and `useBriefingStyle` hooks.

### 2. Type Definitions
- `LayoutTemplate` previously included optional `margins`.
- `LayoutBlock` included `isFullBleed` to bypass margins.

### 3. Editor UI and Canvas Rendering
- **Global Settings**: Included sliders for vertical and horizontal margins.
- **CanvasArtboard**: Subtracted margins from `contentWidth` and `contentHeight` for block positioning.
- **Reference Lines**: Dashed boundaries rendered in the editor to indicate margin constraints.

### 4. Export Services
- `exportToPSD`, `exportToSVG`, and AI bridging services previously required coordinate transformations:
  `const x = (block.x / 100) * (W - margins.left - margins.right) + margins.left;`

## Removal Logic
1. **Clean up Store**: Removed all margin-related state and actions.
2. **Simplified Layout Engine**: Modified `CanvasArtboard` and export services to map block percentages directly to the full `canvasSize` (effectively setting margins to 0).
3. **UI/UX Cleanup**: Removed sliders from sidebar settings and dashed reference lines from the workspace.
4. **Export Simplification**: Exports now use direct percentage-to-pixel mapping without offsets.
