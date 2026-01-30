---
title: Highlight Areas
impact: MEDIUM
impactDescription: useful for teaching box positions
tags: styling, highlight, highlightAreas, areas
---

## Highlight Areas

Use `highlightAreas()` to draw rectangles around fretboard regions.

**Incorrect (wrong area format):**

```javascript
// Areas need two positions: top-left and bottom-right corners
fretboard.highlightAreas(
  { string: 1, fret: 5 }, // Missing second position!
);
```

**Correct (highlight single area):**

```javascript
fretboard
  .renderScale({ type: "major", root: "G" })
  .style({
    fill: ({ degree }) => (degree === 1 ? "#ff6b6b" : "white"),
  })
  .highlightAreas([
    { string: 1, fret: 5 }, // Top-right corner
    { string: 6, fret: 2 }, // Bottom-left corner
  ]);
```

**Correct (multiple highlight areas):**

```javascript
fretboard.renderScale({ type: "major", root: "G" }).highlightAreas(
  // First box
  [
    { string: 1, fret: 5 },
    { string: 6, fret: 2 },
  ],
  // Second box
  [
    { string: 1, fret: 10 },
    { string: 6, fret: 7 },
  ],
);

// Clear highlights later
fretboard.clearHighlightAreas();
```

**Highlight styling options (set in Fretboard constructor):**

```javascript
const fretboard = new Fretboard({
  el: "#fretboard",
  highlightPadding: 10, // Padding around area
  highlightRadius: 10, // Corner radius
  highlightStroke: "transparent", // Border color
  highlightFill: "dodgerblue", // Fill color
  highlightBlendMode: "color-burn", // CSS blend mode
});
```
