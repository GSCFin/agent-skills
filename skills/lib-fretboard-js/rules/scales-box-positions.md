---
title: Render Box Positions
impact: MEDIUM
impactDescription: focused position practice
tags: scales, boxes, renderBox, FretboardSystem
---

## Render Box Positions

Use `renderBox()` to display only the notes within a specific box position.

**Incorrect (using renderScale when you want box only):**

```javascript
// renderScale shows ALL scale notes, with box notes highlighted
fretboard.renderScale({
  type: "major",
  root: "C",
  box: { system: Systems.CAGED, box: "C" },
});
// This shows entire scale with C box highlighted - may be cluttered
```

**Correct (renderBox for focused display):**

```javascript
// renderBox shows ONLY the notes in the box position
fretboard.renderBox({
  type: "major",
  root: "C",
  box: {
    system: Systems.CAGED,
    box: "C",
  },
});
// Only shows notes in the C-shaped position
```

**Correct (using FretboardSystem for custom filtering):**

```javascript
import { Fretboard, FretboardSystem, Systems } from "@moonwave99/fretboard.js";

const system = new FretboardSystem();

// Get all scale positions with box info
const positions = system.getScale({
  type: "major",
  root: "C",
  box: {
    system: Systems.CAGED,
    box: "C",
  },
});

// Each position has { string, fret, note, interval, inBox, ... }
const boxPositions = positions.filter((p) => p.inBox);

const fretboard = new Fretboard({ el: "#fretboard" });
fretboard.setDots(boxPositions).render();
```
