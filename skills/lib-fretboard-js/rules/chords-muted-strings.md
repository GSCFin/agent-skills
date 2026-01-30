---
title: Show Muted Strings
impact: MEDIUM
impactDescription: improves chord diagram clarity
tags: chords, muted, strings, muteStrings
---

## Show Muted Strings

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
