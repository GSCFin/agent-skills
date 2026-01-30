---
title: Add Barre Indicators
impact: HIGH
impactDescription: essential for barre chord visualization
tags: chords, barre, fingering
---

## Add Barre Indicators

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
