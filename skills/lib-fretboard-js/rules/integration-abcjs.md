---
title: Integrate with ABCJS
impact: LOW
impactDescription: specialized use case for notation sync
tags: integration, abcjs, notation, playback, sync
---

## Integrate with ABCJS

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
