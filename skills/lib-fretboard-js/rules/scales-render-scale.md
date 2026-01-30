---
title: Display Scale Patterns
impact: HIGH
impactDescription: essential for scale visualization
tags: scales, renderScale, modes, patterns
---

## Display Scale Patterns

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
