---
title: Generate Tetrachord Patterns
impact: LOW
impactDescription: useful for scale construction teaching
tags: tetrachords, patterns, TetrachordTypes, TetrachordLayouts
---

## Generate Tetrachord Patterns

Use `tetrachord()` to generate four-note patterns for scale building.

**Incorrect (wrong layout for starting fret):**

```javascript
import {
  tetrachord,
  TetrachordTypes,
  TetrachordLayouts,
} from "@moonwave99/fretboard.js";

// OnePlusThree layout from fret 0 causes negative frets
const pattern = tetrachord({
  root: "E",
  string: 6,
  fret: 0,
  type: TetrachordTypes.Major,
  layout: TetrachordLayouts.OnePlusThree, // Error!
});
```

**Correct (linear tetrachord):**

```javascript
import {
  Fretboard,
  tetrachord,
  TetrachordTypes,
  TetrachordLayouts,
} from "@moonwave99/fretboard.js";

// Generate linear tetrachord on one string
const lowerTetrachord = tetrachord({
  root: "E",
  string: 6,
  fret: 0,
  type: TetrachordTypes.Major,
  layout: TetrachordLayouts.Linear,
});
// Returns: [{ string: 6, fret: 0, note: 'E' }, { string: 6, fret: 2, note: 'F#' }, ...]

const fretboard = new Fretboard({
  el: "#fretboard",
  dotText: ({ note }) => note,
});

fretboard.setDots(lowerTetrachord).render();
```

**Correct (two tetrachords forming a scale):**

```javascript
// Major scale = Major tetrachord + Major tetrachord
const lower = tetrachord({
  root: "E",
  string: 5,
  fret: 7,
  type: TetrachordTypes.Major,
  layout: TetrachordLayouts.ThreePlusOne,
});

const upper = tetrachord({
  root: "B",
  string: 4,
  fret: 9,
  type: TetrachordTypes.Major,
  layout: TetrachordLayouts.ThreePlusOne,
});

fretboard
  .setDots([...lower, ...upper])
  .render()
  .style({
    fill: (dot, index) => (index < 4 ? "#ffd43b" : "#ff6b6b"),
  });
```

**Tetrachord types:**

- `TetrachordTypes.Major` - W-W-H (major scale)
- `TetrachordTypes.Minor` - W-H-W (natural minor)
- `TetrachordTypes.Phrygian` - H-W-W (phrygian mode)
- `TetrachordTypes.Harmonic` - H-A-H (harmonic minor)
- `TetrachordTypes.Lydian` - W-W-W (lydian mode)

**Tetrachord layouts:**

- `TetrachordLayouts.Linear` - All on one string
- `TetrachordLayouts.ThreePlusOne` - 3 notes on first string, 1 on next
- `TetrachordLayouts.TwoPlusTwo` - 2 notes on each string
- `TetrachordLayouts.OnePlusThree` - 1 note on first string, 3 on next
