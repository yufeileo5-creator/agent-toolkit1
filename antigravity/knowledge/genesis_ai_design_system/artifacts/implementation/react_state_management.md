# React State Management and Async Callbacks

In complex interactive components like the **Layout Editor**, maintaining state synchronization across asynchronous boundaries (e.g., `setTimeout`, `callbacks`, `Portals`) is critical. This project has identified and solved common React "stale closure" issues.

## The Stale Closure Problem

When a function like `handleGenerate` is defined inside a component, it "captures" the state variables (like `template`) at the time of its creation. If this function is passed to a child component and called inside a `setTimeout` after a state update (like `setTemplate`), the function may still be executing with the *old* state value because the closure was not refreshed.

### Real-world scenario in Layout Editor:
1. User clicks "Generate Briefing" inside `LayoutEditorModal`.
2. `LayoutEditorModal` calls `onSave(newData)` -> triggers `setTemplate(newData)` in `App.tsx`.
3. `LayoutEditorModal` calls `setTimeout(() => onGenerate(), 150)`.
4. When `onGenerate` (which is `handleGenerate`) finally runs in `App.tsx`, `template.blocks` might still appear empty because it's reading the stale value from the previous render cycle.

## Solution: `useRef` Synchronization

To ensure asynchronous callbacks always access the most up-to-date state, the project uses a `useRef` to maintain a live reference to the state.

```typescript
// Pattern used in App.tsx
const [template, setTemplate] = useState<LayoutTemplate>(INITIAL_DATA);

// Create a ref that always points to the current state
const templateRef = useRef(template);

// Sync the ref on every state change
useEffect(() => { 
  templateRef.current = template; 
}, [template]);

const handleGenerate = async () => {
  // Always read from current property of the ref
  const currentTemplate = templateRef.current;
  const currentImages = extractedImagesRef.current;
  
  if (currentTemplate.blocks.length === 0) return;
  // ... proceed with currentTemplate and currentImages
};
```

This pattern is applied to both `template` (layout structure) and `extractedImages` (document images) to ensure the asynchronous generation logic always has the final data after user edits and doc uploads.


## Timing Considerations for Modal Interactions

When saving and immediately triggering an action from a modal:
- **Immediate Closure**: Calling `onClose()` immediately after `onSave()` can lead to race conditions where the parent component unmounts the modal before processing the save.
- **Improved Flow**: 
  1. `onSave(data)`
  2. `onClose()` (immediate or slightly delayed)
  3. `setTimeout(() => onGenerate(), duration)` to ensure the parent state has reconciled before the next heavy async task (like API generation) begins.

## State Update Race Conditions (Batching)

In asynchronous flows like `handleGenerate`, calling a state setter twice for the same state (e.g., `setBriefingData`) within the same execution cycle can lead to the first update being lost or creating a flickered UI state.

**The "Overwrite" Trap:**
1. `setBriefingData(response.data)` is called (initializing from API).
2. Local logic then modifies `response.data` (e.g., populating images).
3. `setBriefingData(updatedData)` is called.

**Solution: Unified Final Data**
Calculate the final state object completely before calling the setter once.
```typescript
let finalData = response.data;
if (hasImages) {
  finalData = populateImages(response.data, images);
}
setBriefingData(finalData); // Single authoritative update
```
This ensures React batches only a single render with the correct final data, avoiding race conditions and redundant renders.
