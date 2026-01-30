---
title: Render Chord Diagrams
impact: HIGH
impactDescription: most common use case for chord visualization
tags: chords, diagram, fingering, renderChord
---

## Render Chord Diagrams

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
