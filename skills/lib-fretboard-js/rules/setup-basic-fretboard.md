---
title: Create Basic Fretboard
impact: CRITICAL
impactDescription: foundation for all visualizations
tags: setup, configuration, options, tuning
---

## Create Basic Fretboard

Configure a Fretboard instance with appropriate options for your use case.

**Incorrect (no container element or wrong tuning):**

```javascript
// Missing el option - where should the SVG render?
const fretboard = new Fretboard({
  fretCount: 12,
});
// Error: Cannot read properties of null

// Mismatched stringCount and tuning length
const fretboard = new Fretboard({
  el: "#fretboard",
  stringCount: 6,
  tuning: ["E2", "A2", "D3", "G3"], // Only 4 strings!
});
// Error: stringCount (6) and tuning size (4) do not match
```

**Correct (basic configuration):**

```javascript
import { Fretboard, GUITAR_TUNINGS } from "@moonwave99/fretboard.js";

const fretboard = new Fretboard({
  el: "#fretboard", // CSS selector or DOM element
  tuning: GUITAR_TUNINGS.default, // ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
  stringCount: 6,
  fretCount: 15,
  width: 960,
  height: 150,
  showFretNumbers: true,
  dotSize: 20,
  dotFill: "white",
  dotStrokeColor: "#555",
  font: "Arial",
});

fretboard.render(); // Renders empty fretboard
```

**Correct (chord diagram configuration):**

```javascript
// Smaller dimensions for chord diagrams
const chordFretboard = new Fretboard({
  el: "#chord-diagram",
  width: 300,
  height: 200,
  fretCount: 5,
  scaleFrets: false, // Equal fret spacing for chord diagrams
  showFretNumbers: true,
  crop: true, // Crop to show only used frets
  fretLeftPadding: 1, // Extra fret before first note
  dotSize: 25,
});
```

**Common configuration options:**

| Option            | Type            | Default         | Description                     |
| ----------------- | --------------- | --------------- | ------------------------------- |
| `el`              | string/Element  | `'#fretboard'`  | Container selector or element   |
| `tuning`          | string[]        | Standard tuning | Array of note names with octave |
| `stringCount`     | number          | 6               | Number of strings               |
| `fretCount`       | number          | 15              | Number of frets to display      |
| `width`           | number          | 960             | SVG width in pixels             |
| `height`          | number          | 150             | SVG height in pixels            |
| `scaleFrets`      | boolean         | true            | Use realistic fret scaling      |
| `crop`            | boolean         | false           | Crop to show only used frets    |
| `showFretNumbers` | boolean         | true            | Show fret numbers below         |
| `dotSize`         | number          | 20              | Diameter of position dots       |
| `dotFill`         | string/function | 'white'         | Dot fill color                  |
| `dotText`         | function        | () => ''        | Function returning dot label    |

**Preset tunings:**

- `GUITAR_TUNINGS.default` - E A D G B E (standard)
- `GUITAR_TUNINGS.halfStepDown` - Eb Ab Db Gb Bb Eb
- `GUITAR_TUNINGS.dropD` - D A D G B E
- `GUITAR_TUNINGS.openG` - D G D G B D
- `GUITAR_TUNINGS.DADGAD` - D A D G A D
