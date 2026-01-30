# fretboard.js Best Practices

**Version 1.0.0**  
Based on fretboard.js v0.2.12  
January 2026

> **Note:**  
> This document is mainly for agents and LLMs to follow when implementing,  
> generating, or maintaining fretboard visualization code. Humans may also find  
> it useful, but guidance here is optimized for automation and consistency by  
> AI-assisted workflows.

---

## Abstract

Comprehensive guide for the fretboard.js library - a guitar/bass fretboard SVG
visualization toolkit. Contains 14 rules across 6 categories, prioritized by
impact from critical (Setup, Chord/Scale Rendering) to lower priority (Advanced
patterns). Each rule includes detailed explanations, real-world examples
comparing incorrect vs. correct implementations, and API configuration options.

---

## Table of Contents

1. [Setup](#1-setup) — **CRITICAL**
   - 1.1 [Install and Import fretboard.js](#11-install-and-import-fretboardjs)
   - 1.2 [Create Basic Fretboard](#12-create-basic-fretboard)
2. [Chord Rendering](#2-chord-rendering) — **HIGH**
   - 2.1 [Render Chord Diagrams](#21-render-chord-diagrams)
   - 2.2 [Add Barre Indicators](#22-add-barre-indicators)
   - 2.3 [Show Muted Strings](#23-show-muted-strings)
3. [Scale Rendering](#3-scale-rendering) — **HIGH**
   - 3.1 [Display Scale Patterns](#31-display-scale-patterns)
   - 3.2 [Use Scale Systems](#32-use-scale-systems)
   - 3.3 [Render Box Positions](#33-render-box-positions)
4. [Styling](#4-styling) — **MEDIUM**
   - 4.1 [Customize Dot Appearance](#41-customize-dot-appearance)
   - 4.2 [Highlight Areas](#42-highlight-areas)
5. [Events](#5-events) — **MEDIUM**
   - 5.1 [Add Mouse Event Handlers](#51-add-mouse-event-handlers)
   - 5.2 [Track Position Information](#52-track-position-information)
6. [Advanced](#6-advanced) — **LOW**
   - 6.1 [Generate Tetrachord Patterns](#61-generate-tetrachord-patterns)
   - 6.2 [Integrate with ABCJS](#62-integrate-with-abcjs)

---

## 1. Setup

**Impact: CRITICAL**

Essential setup and configuration for using fretboard.js in your project.

### 1.1 Install and Import fretboard.js

**Impact: CRITICAL (required for any fretboard visualization)**

Install fretboard.js and its peer dependencies to enable fretboard visualization.

**Incorrect (missing dependencies or wrong import):**

```javascript
// Missing d3-selection dependency causes runtime error
import { Fretboard } from "fretboard.js";

const fretboard = new Fretboard(); // Error: d3 is not defined
```

**Correct (npm installation with ESM import):**

```javascript
// First install: npm install @moonwave99/fretboard.js

// ESM import (recommended)
import { Fretboard, Systems, GUITAR_TUNINGS } from "@moonwave99/fretboard.js";

// Create fretboard instance
const fretboard = new Fretboard({
  el: "#fretboard-container",
});
```

**Alternative (CDN/UMD for browser):**

```html
<script src="https://unpkg.com/@moonwave99/fretboard.js/dist/fretboard.umd.js"></script>
<script>
  const { Fretboard, Systems } = window.Fretboard;
  const fretboard = new Fretboard({ el: "#fretboard" });
</script>
```

**Available exports:**

- `Fretboard` - Main visualization class
- `FretboardSystem` - Music theory system for scales/positions
- `Systems` - Enum: CAGED, TNPS, pentatonic
- `GUITAR_TUNINGS` - Preset tunings (default, dropD, openG, etc.)
- `tetrachord`, `TetrachordTypes`, `TetrachordLayouts` - Tetrachord helpers
- `disableStrings`, `disableDots`, `sliceBox` - Position manipulation tools

Reference: [https://moonwave99.github.io/fretboard.js/](https://moonwave99.github.io/fretboard.js/)

---

### 1.2 Create Basic Fretboard

**Impact: CRITICAL (foundation for all visualizations)**

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

---

## 2. Chord Rendering

**Impact: HIGH**

Methods for rendering chord diagrams with fingerings, barres, and muted strings.

### 2.1 Render Chord Diagrams

**Impact: HIGH (most common use case for chord visualization)**

Use `renderChord()` to display chord shapes with proper fingering positions.

**Incorrect (wrong chord string format):**

```javascript
// Chord format must use 'x' for muted, numbers for frets
fretboard.renderChord("x-3-2-0-1-0"); // Correct format with dashes
fretboard.renderChord("X32010"); // Works but capital X may confuse

// Don't pass array - use string format
fretboard.renderChord([null, 3, 2, 0, 1, 0]); // Wrong!
```

**Correct (standard chord format):**

```javascript
// Open chords - 'x' for muted, '0' for open, numbers for fret
fretboard.renderChord("x32010"); // C major
fretboard.renderChord("320003"); // G major
fretboard.renderChord("022100"); // E major

// Use dashes for multi-digit frets (above 9th fret)
fretboard.renderChord("x-10-9-10-x-x"); // F#m7 at 9th position
```

**Correct (with cropping for position diagrams):**

```javascript
const fretboard = new Fretboard({
  el: "#chord",
  width: 300,
  height: 200,
  fretCount: 4,
  scaleFrets: false,
  showFretNumbers: true,
  crop: true, // Crop unused frets
  fretLeftPadding: 1, // Show one extra fret before first note
});

// Barre chord at 5th fret - will show frets 5-8
fretboard.renderChord("577655"); // A major barre
```

The chord string is read from lowest string (6th) to highest (1st). Each character represents the fret number, with 'x' for muted strings.

---

### 2.2 Add Barre Indicators

**Impact: HIGH (essential for barre chord visualization)**

Add barre indicators to show finger barring across multiple strings.

**Incorrect (barre without proper stringFrom/stringTo):**

```javascript
// Missing barre configuration - dots shown but no barre bar
fretboard.renderChord("133211"); // F major - no barre shown!
```

**Correct (single barre):**

```javascript
// renderChord accepts optional barre configuration
fretboard.renderChord("133211", {
  fret: 1, // Full barre at fret 1 (all strings)
});

// Partial barre (e.g., for Bm: x24432)
fretboard.renderChord("x24432", {
  fret: 2,
  stringFrom: 5, // Barre from 5th string to 1st
});
```

**Correct (multiple barres):**

```javascript
// Some chord shapes require multiple barres
fretboard.renderChord("x35553", [
  { fret: 3, stringFrom: 5 }, // Lower barre
  { fret: 5, stringFrom: 4, stringTo: 2 }, // Upper partial barre
]);

// A7#9 (Hendrix chord)
fretboard.renderChord("x75678", [
  { fret: 5, stringTo: 4 },
  { fret: 8, stringFrom: 2 },
]);
```

**Barre configuration options:**

| Option       | Type   | Default            | Description              |
| ------------ | ------ | ------------------ | ------------------------ |
| `fret`       | number | required           | Fret position for barre  |
| `stringFrom` | number | 6 (or stringCount) | Starting string (lowest) |
| `stringTo`   | number | 1                  | Ending string (highest)  |

---

### 2.3 Show Muted Strings

**Impact: MEDIUM (improves chord diagram clarity)**

Use `muteStrings()` to add X markers for muted strings.

**Incorrect (manually trying to style muted strings):**

```javascript
// Don't try to manually add X markers
fretboard.renderChord("x32010");
// X for muted string 6 is not shown!
```

**Correct (muteStrings is called automatically by renderChord):**

```javascript
// renderChord automatically handles muted strings from 'x' in chord string
fretboard.renderChord("x32010"); // X for string 6 is added automatically

// For manual control, use muteStrings() after setDots()
fretboard
  .setDots([
    { string: 5, fret: 3 },
    { string: 4, fret: 2 },
    { string: 2, fret: 1 },
  ])
  .render()
  .muteStrings({
    strings: [6, 3], // Mute strings 6 and 3
    width: 15, // X marker size
    strokeWidth: 5, // Line thickness
    stroke: "#333", // X color
  });
```

**Note:** When using `renderChord()`, muted strings are automatically detected from 'x' characters in the chord string and `muteStrings()` is called internally.

---

## 3. Scale Rendering

**Impact: HIGH**

Methods for displaying scale patterns using various box systems.

### 3.1 Display Scale Patterns

**Impact: HIGH (essential for scale visualization)**

Use `renderScale()` to display scale notes across the entire fretboard.

**Incorrect (wrong scale name or missing root):**

```javascript
// Scale type must be a valid tonal.js scale name
fretboard.renderScale({
  type: "Major", // Should be lowercase
  root: "C",
});

// Missing root note
fretboard.renderScale({ type: "major" }); // Root defaults to C but be explicit
```

**Correct (basic scale rendering):**

```javascript
import { Fretboard } from "@moonwave99/fretboard.js";

const fretboard = new Fretboard({
  el: "#fretboard",
  dotText: ({ note }) => note, // Show note names
});

// Render C major scale across entire fretboard
fretboard.renderScale({
  type: "major",
  root: "C",
});

// Minor pentatonic
fretboard.renderScale({
  type: "minor pentatonic",
  root: "A",
});

// Modes - use mode name directly
fretboard.renderScale({
  type: "dorian",
  root: "D",
});
```

**Correct (with dynamic styling):**

```javascript
const fretboard = new Fretboard({
  el: "#fretboard",
  dotText: ({ note, octave }) => `${note}${octave}`,
  dotFill: ({ interval }) => (interval === "1P" ? "#ff6b6b" : "white"), // Highlight root notes
});

fretboard.renderScale({
  type: "major",
  root: "G",
});
```

**Common scale types (from tonal.js):**

- `major`, `minor`, `harmonic minor`, `melodic minor`
- `major pentatonic`, `minor pentatonic`
- `ionian`, `dorian`, `phrygian`, `lydian`, `mixolydian`, `aeolian`, `locrian`
- `blues`, `whole tone`, `diminished`

---

### 3.2 Use Scale Systems

**Impact: HIGH (enables position-based practice)**

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

---

### 3.3 Render Box Positions

**Impact: MEDIUM (focused position practice)**

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

---

## 4. Styling

**Impact: MEDIUM**

Customize the visual appearance of fretboard diagrams.

### 4.1 Customize Dot Appearance

**Impact: MEDIUM (improves visual clarity and information)**

Use `style()` method or configuration functions to customize dot appearance.

**Incorrect (trying to style after render without style method):**

```javascript
// CSS doesn't easily target specific dots
fretboard.renderScale({ type: "major", root: "C" });
document.querySelectorAll(".dot").forEach((el) => {
  el.style.fill = "red"; // This won't work properly
});
```

**Correct (configuration functions):**

```javascript
const fretboard = new Fretboard({
  el: "#fretboard",

  // Function receives position object, returns value
  dotFill: ({ interval, inBox }) => {
    if (interval === "1P") return "#ff6b6b"; // Root = red
    if (!inBox) return "#ccc"; // Outside box = gray
    return "white"; // In box = white
  },

  dotText: ({ note, interval }) => (interval === "1P" ? note : ""), // Only label roots

  dotStrokeColor: ({ interval }) => (interval === "1P" ? "#c92a2a" : "#555"),
});

fretboard.renderScale({
  type: "major",
  root: "G",
  box: { system: Systems.CAGED, box: "E" },
});
```

**Correct (style method for post-render updates):**

```javascript
fretboard
  .renderScale({ type: "major", root: "C" })
  .style({
    // Filter which dots to style
    filter: { interval: "1P" }, // Only root notes

    // Properties to change
    fill: "#ff6b6b",
    text: ({ note }) => note,
    fontSize: 14,
    fontFill: "white",
  })
  .style({
    // Style thirds differently
    filter: ({ degree }) => degree === 3,
    fill: "#4dabf7",
    text: ({ note }) => note,
  });
```

**Style method options:**

| Option         | Type            | Description         |
| -------------- | --------------- | ------------------- |
| `filter`       | object/function | Which dots to style |
| `fill`         | string          | Dot fill color      |
| `stroke`       | string          | Dot stroke color    |
| `stroke-width` | number          | Stroke width        |
| `text`         | function        | Dot label function  |
| `fontSize`     | number          | Label font size     |
| `fontFill`     | string          | Label color         |

---

### 4.2 Highlight Areas

**Impact: MEDIUM (useful for teaching box positions)**

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

---

## 5. Events

**Impact: MEDIUM**

Add interactive features with mouse and pointer events.

### 5.1 Add Mouse Event Handlers

**Impact: MEDIUM (enables interactive applications)**

Use `on()` method to add event handlers for user interaction.

**Incorrect (trying to add events to SVG directly):**

```javascript
// SVG elements are inside wrapper - complex to target
document.querySelector("#fretboard svg").addEventListener("click", (e) => {
  // Hard to determine which fret/string was clicked
});
```

**Correct (using on method):**

```javascript
const fretboard = new Fretboard({
  el: "#fretboard",
  dotText: ({ note }) => note,
});

fretboard.render();

// Click handler - receives position object and event
fretboard.on("click", (position, event) => {
  console.log(
    `Clicked: ${position.note} at string ${position.string}, fret ${position.fret}`,
  );
});

// Hover tracking
fretboard.on("mousemove", (position, event) => {
  console.log(`Hovering: ${position.note}`);
});

// Mouse enter/leave
fretboard.on("mouseenter", (position, event) => {
  document.body.classList.add("fretboard-active");
});

fretboard.on("mouseleave", (position, event) => {
  document.body.classList.remove("fretboard-active");
});
```

**Correct (interactive note selection):**

```javascript
let selectedDots = [];

const fretboard = new Fretboard({
  el: "#fretboard",
  dotText: ({ note }) => note,
});

fretboard.render();

fretboard.on("click", ({ string, fret, note }) => {
  // Check if already selected
  const existingIndex = selectedDots.findIndex(
    (d) => d.string === string && d.fret === fret,
  );

  if (existingIndex > -1) {
    // Remove if already selected
    selectedDots.splice(existingIndex, 1);
  } else {
    // Add new selection
    selectedDots.push({ string, fret, note });
  }

  // Re-render with updated dots
  fretboard.setDots(selectedDots).render();
});

// Clear all button
clearButton.addEventListener("click", () => {
  selectedDots = [];
  fretboard.clear();
});
```

**Supported events:** `click`, `mousemove`, `mouseenter`, `mouseleave`

---

### 5.2 Track Position Information

**Impact: MEDIUM (enables note identification features)**

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

---

## 6. Advanced

**Impact: LOW**

Advanced patterns for specific use cases.

### 6.1 Generate Tetrachord Patterns

**Impact: LOW (useful for scale construction teaching)**

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

---

### 6.2 Integrate with ABCJS

**Impact: LOW (specialized use case for notation sync)**

Synchronize fretboard visualization with ABCJS music notation playback.

**Incorrect (not using synth callbacks):**

```javascript
// ABCJS rendered but fretboard not updated during playback
ABCJS.renderAbc("notation", abcString);
// No connection to fretboard!
```

**Correct (sync with ABCJS playback):**

```javascript
import ABCJS from "abcjs";
import { Fretboard, Systems } from "@moonwave99/fretboard.js";
import { getChord } from "@tonaljs/chord";

const fretboard = new Fretboard({
  el: "#fretboard",
  dotFill: ({ inBox }) => (inBox ? "white" : "#ccc"),
}).renderScale({
  root: "C",
  box: { system: Systems.CAGED, box: "E" },
});

// Render ABC notation with click handler
const visualObj = ABCJS.renderAbc("notation", abcString, {
  clickListener: (element) => {
    if (!element.chord) return;

    const [root, chordType] = [
      element.chord[0].name[0],
      element.chord[0].name.substring(1),
    ];
    const chord = getChord(chordType, `${root}3`);

    // Highlight chord tones on fretboard
    fretboard.style({
      filter: { inBox: true },
      stroke: ({ note, octave }) =>
        chord.notes.includes(`${note}${octave}`) ? "#ff6b6b" : "#555",
    });
  },
})[0];

// Setup synth with playback callbacks
const synthControl = new ABCJS.synth.SynthController();
synthControl.load("#audio", {
  onEvent: ({ midiPitches, elements }) => {
    const playedNote = ABCJS.synth.pitchToNoteName[midiPitches[0].pitch];

    // Highlight currently playing note
    fretboard.style({
      filter: { inBox: true },
      fill: ({ note, octave }) =>
        `${note}${octave}` === playedNote ? "#ff6b6b" : "white",
    });
  },
});

synthControl.setTune(visualObj, false);
```

**Key integration points:**

1. Use `clickListener` in ABCJS render options for click-to-highlight
2. Use `onEvent` callback in SynthController for playback sync
3. Use `@tonaljs/chord` to parse chord names and get chord tones
4. Use fretboard `style()` method to update highlight dynamically

---

## References

1. [https://moonwave99.github.io/fretboard.js/](https://moonwave99.github.io/fretboard.js/) - Official documentation
2. [https://github.com/moonwave99/fretboard.js](https://github.com/moonwave99/fretboard.js) - GitHub repository
3. [https://github.com/tonaljs/tonal](https://github.com/tonaljs/tonal) - tonal.js music theory library
4. [https://www.abcjs.net/](https://www.abcjs.net/) - ABCJS notation library
