---
title: Track Position Information
impact: MEDIUM
impactDescription: enables note identification features
tags: events, position, getNoteAtPosition, FretboardSystem
---

## Track Position Information

Access note and position information from event handlers.

**Incorrect (not using the position object):**

```javascript
fretboard.on("click", (position) => {
  // Position object has note info, don't recalculate
  const note = calculateNoteFromPosition(position.string, position.fret);
});
```

**Correct (using position properties):**

```javascript
fretboard.on("click", (position, event) => {
  // Position object contains:
  const {
    string, // 1-6 (1 = high E)
    fret, // 0-15 (0 = open)
    note, // 'C', 'F#', etc.
    chroma, // 0-11 (pitch class)
  } = position;

  console.log(`String ${string}, Fret ${fret}: ${note} (chroma: ${chroma})`);
});
```

**Correct (using FretboardSystem for more info):**

```javascript
import { Fretboard, FretboardSystem } from "@moonwave99/fretboard.js";

const system = new FretboardSystem();
const fretboard = new Fretboard({ el: "#fretboard" });

fretboard.on("click", (position) => {
  // Get full note info including octave
  const noteInfo = system.getNoteAtPosition(position);

  console.log(`${noteInfo.note}${noteInfo.octave}`);
  // e.g., "C4", "G3"
});
```

**Position object properties:**

| Property | Type   | Description                                |
| -------- | ------ | ------------------------------------------ |
| `string` | number | String number (1 = high, 6 = low)          |
| `fret`   | number | Fret number (0 = open)                     |
| `note`   | string | Note name without octave                   |
| `chroma` | number | Pitch class 0-11 (C=0, C#=1, etc.)         |
| `octave` | number | Octave number (when using FretboardSystem) |
