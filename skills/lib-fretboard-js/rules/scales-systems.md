---
title: Use Scale Systems
impact: HIGH
impactDescription: enables position-based practice
tags: scales, CAGED, TNPS, pentatonic, systems, boxes
---

## Use Scale Systems

Use CAGED, TNPS, or pentatonic box systems to show scale positions.

**Incorrect (wrong system or box value):**

```javascript
import { Systems } from "@moonwave99/fretboard.js";

// Box value must match system type
fretboard.renderScale({
  type: "major",
  root: "C",
  box: {
    system: Systems.CAGED,
    box: 1, // CAGED uses 'C', 'A', 'G', 'E', 'D' - not numbers!
  },
});

// TNPS uses numbers 1-7, not letters
fretboard.renderScale({
  type: "major",
  root: "C",
  box: {
    system: Systems.TNPS,
    box: "C", // Wrong! TNPS uses 1-7
  },
});
```

**Correct (CAGED system):**

```javascript
import { Fretboard, Systems } from "@moonwave99/fretboard.js";

const fretboard = new Fretboard({
  el: "#fretboard",
  dotFill: ({ inBox }) => (inBox ? "white" : "#ddd"), // Dim notes outside box
  dotText: ({ note }) => note,
});

// C-shaped box of C major scale
fretboard.renderScale({
  type: "major",
  root: "C",
  box: {
    system: Systems.CAGED,
    box: "C", // Options: 'C', 'A', 'G', 'E', 'D'
  },
});
```

**Correct (TNPS - Three Notes Per String):**

```javascript
// TNPS system uses numbered patterns 1-7
fretboard.renderScale({
  type: "major",
  root: "C",
  box: {
    system: Systems.TNPS,
    box: 1, // Options: 1, 2, 3, 4, 5, 6, 7
  },
});
```

**Correct (Pentatonic boxes):**

```javascript
// Pentatonic system uses numbered boxes 1-5
fretboard.renderScale({
  type: "minor pentatonic",
  root: "E",
  box: {
    system: Systems.pentatonic,
    box: 1, // Options: 1, 2, 3, 4, 5
  },
});
```

**System comparison:**

| System     | Box Values    | Notes/String   | Best For               |
| ---------- | ------------- | -------------- | ---------------------- |
| CAGED      | C, A, G, E, D | Variable       | Chord-scale connection |
| TNPS       | 1-7           | 3 (consistent) | Speed/legato playing   |
| pentatonic | 1-5           | 2-3            | Blues/rock soloing     |
