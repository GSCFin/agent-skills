---
name: abcjs
description: JavaScript library for rendering ABC music notation as SVG and playing it as audio. Use when implementing music notation rendering, audio playback, interactive music editors, or animation synchronized with music. Triggers on tasks involving ABC notation, sheet music display, music synthesis, or MIDI generation.
argument-hint: <abc-notation-string-or-file>
metadata:
  author: paulrosen
  version: '6.6.0'
  license: MIT
  docs: https://docs.abcjs.net
  repo: https://github.com/paulrosen/abcjs
---

# abcjs - Music Notation Library

JavaScript library for rendering standard music notation in the browser using ABC notation format. Provides SVG rendering, audio synthesis, live editing, and playback animation.

## Reference Implementation

Full source code: `reference/abcjs/`

## Installation

```bash
npm install abcjs
```

CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/abcjs@6/dist/abcjs-basic-min.js"></script>
```

---

## ABC Notation Reference

ABC is a text-based music notation format. Full standard: [abcnotation.com](http://abcnotation.com/learn)

### Header Fields

```abc
X: 1                    % Reference number (required)
T: Tune Title           % Title
C: Composer Name        % Composer
M: 4/4                  % Meter (time signature)
L: 1/8                  % Default note length
Q: 1/4=120              % Tempo (quarter=120 bpm)
K: G                    % Key signature (required, last header)
```

### Notes

| Notation        | Description            |
| --------------- | ---------------------- |
| `C D E F G A B` | Notes in lower octave  |
| `c d e f g a b` | Notes in middle octave |
| `C, D,`         | Octave down (comma)    |
| `c' d'`         | Octave up (apostrophe) |
| `^C`            | Sharp                  |
| `_B`            | Flat                   |
| `=C`            | Natural                |

### Note Lengths

| Notation      | Description   |
| ------------- | ------------- |
| `C2`          | Double length |
| `C/2` or `C/` | Half length   |
| `C3/2`        | Dotted (1.5x) |
| `C4`          | 4x length     |

### Rests

| Notation | Description           |
| -------- | --------------------- |
| `z`      | Rest (default length) |
| `z2`     | Rest (double length)  |
| `x`      | Invisible rest        |

### Chords and Groupings

| Notation | Description                |
| -------- | -------------------------- |
| `[CEG]`  | Chord (simultaneous notes) |
| `"Am"C`  | Chord symbol above note    |
| `(CDE)`  | Slur                       |
| `C-C`    | Tie                        |
| `{g}A`   | Grace note                 |

### Bar Lines

| Notation | Description   |
| -------- | ------------- | -------------------- |
| `\|`     | Single bar    |
| `\|\|`   | Double bar    |
| `\|:`    | Start repeat  |
| `:\|`    | End repeat    |
| `\|1`    | First ending  |
| `\|2`    | Second ending |
| `[       | `             | Thick-thin bar       |
| `        | ]`            | Thin-thick bar (end) |

### Decorations

| Notation           | Description          |
| ------------------ | -------------------- |
| `!p!` `!f!` `!ff!` | Dynamics             |
| `!>!`              | Accent               |
| `!fermata!`        | Fermata              |
| `!trill!`          | Trill                |
| `!mark!`           | Add "mark" CSS class |

### Alternate Note Heads

In `K:` or `V:` lines:

```abc
K:C style=rhythm      % Rhythm slashes
K:C style=harmonic    % Diamond heads
K:C style=x           % X note heads
K:C style=triangle    % Triangle heads
```

Or as decoration: `!style=rhythm!C`

---

## Visual Rendering

### renderAbc()

Main entry point for rendering ABC notation to SVG:

```javascript
import ABCJS from 'abcjs'

// Basic usage
const visualObj = ABCJS.renderAbc('paper', abcString)[0]

// With options
const visualObj = ABCJS.renderAbc('paper', abcString, {
  responsive: 'resize',
  add_classes: true,
  staffwidth: 740,
  wrap: { minSpacing: 1.8, maxSpacing: 2.7, preferredMeasuresPerLine: 4 },
})[0]

// Multiple tunes to multiple elements
ABCJS.renderAbc(['target1', 'target2'], abcString)

// Invisible rendering (audio/analysis only)
const visualObj = ABCJS.renderAbc('*', abcString)[0]
```

### Render Options Reference

| Option            | Default           | Description                           |
| ----------------- | ----------------- | ------------------------------------- |
| `responsive`      | undefined         | `"resize"` for responsive SVG sizing  |
| `staffwidth`      | 740               | Staff width in pixels                 |
| `scale`           | 1                 | Scale factor (0-1 smaller, >1 larger) |
| `add_classes`     | false             | Add CSS classes for styling           |
| `paddingtop`      | 15                | Top padding in pixels                 |
| `paddingbottom`   | 30                | Bottom padding                        |
| `paddingleft`     | 15                | Left padding                          |
| `paddingright`    | 50                | Right padding                         |
| `visualTranspose` | 0                 | Transpose by semitones                |
| `foregroundColor` | currentColor      | Color for all elements                |
| `selectionColor`  | "#ff0000"         | Color for clicked notes               |
| `dragColor`       | same as selection | Color during drag                     |

**Layout Options:**

| Option           | Default   | Description                                                           |
| ---------------- | --------- | --------------------------------------------------------------------- |
| `wrap`           | null      | Line wrapping: `{ minSpacing, maxSpacing, preferredMeasuresPerLine }` |
| `lineBreaks`     | undefined | Array of measure numbers for line breaks                              |
| `oneSvgPerLine`  | false     | Separate SVG per staff system                                         |
| `expandToWidest` | false     | Expand all lines to widest line                                       |
| `stafftopmargin` | 0         | Extra space above each staff                                          |
| `minPadding`     | 0         | Minimum pixels between elements                                       |
| `print`          | false     | Print mode (margins, headers)                                         |

**Feature Options:**

| Option           | Default       | Description                             |
| ---------------- | ------------- | --------------------------------------- |
| `clickListener`  | null          | Callback for note clicks                |
| `dragging`       | false         | Enable note dragging                    |
| `selectTypes`    | false         | Array or `true` for selectable elements |
| `tablature`      | undefined     | Add tablature staff                     |
| `chordGrid`      | undefined     | `"noMusic"` or `"withMusic"`            |
| `jazzchords`     | false         | Jazz-style chord formatting             |
| `germanAlphabet` | false         | German notation (H for B)               |
| `hint_measures`  | false         | Show next measure at line end           |
| `initialClef`    | false         | Show clef only on first line            |
| `accentAbove`    | false         | Place accents above notes               |
| `ariaLabel`      | "Sheet Music" | Accessibility label                     |

**Wrap Option Details:**

```javascript
{
  wrap: {
    minSpacing: 1.8,              // 1 = tight, 2 = double spacing
    maxSpacing: 2.7,              // Max spacing before line break
    preferredMeasuresPerLine: 4,  // Target measures per line
    lastLineLimit: 0.5            // Min fill ratio for last line
  }
}
```

### Return Value (visualObj)

`renderAbc()` returns an array of tune objects. Key properties:

```javascript
const visualObj = ABCJS.renderAbc('paper', abc)[0]

// Data properties
visualObj.formatting // Fonts and formatting commands
visualObj.lines // Array of staff systems
visualObj.metaText // Title, composer, etc.
visualObj.version // Format version
visualObj.visualTranspose // Applied transposition

// Methods
visualObj.getBarLength() // Bar duration (1 = whole note)
visualObj.getBeatLength() // Beat duration
visualObj.getBeatsPerMeasure() // Beats per measure
visualObj.getBpm() // Tempo in BPM
visualObj.getMeter() // Meter object
visualObj.getMeterFraction() // { num: 4, den: 4 }
visualObj.getKeySignature() // Key signature object
visualObj.getPickupLength() // Pickup measure length
visualObj.getTotalBeats() // Total beats (after setUpAudio)
visualObj.getTotalTime() // Total seconds (after setUpAudio)
visualObj.millisecondsPerMeasure() // Ms per measure
visualObj.setUpAudio() // Initialize audio data
visualObj.getElementFromChar(idx) // Element at char position
visualObj.findSelectableElement(el) // Find selectable for element
visualObj.getSelectableArray() // All selectable elements
```

---

## CSS Classes

When `add_classes: true`, elements get classes for styling:

```css
/* Staff lines */
.abcjs-staff { stroke: #ccc; }

/* Notes */
.abcjs-note { fill: black; }
.abcjs-note.abcjs-v0 { } /* Voice 0 */
.abcjs-note.abcjs-l0 { } /* Line 0 */
.abcjs-note.abcjs-mm0 { } /* Measure 0 */

/* Highlight during playback */
.abcjs-note.highlight {
  fill: #00bcd4;
  stroke: #00bcd4;
}

/* Hide finished measures */
.abcjs-mm0.hidden {
  opacity: 0;
  transition: opacity 0.3s;
}

/* Cursor line */
.abcjs-cursor {
  stroke: blue;
  stroke-width: 2;
}

/* Other classes */
.abcjs-bar          /* Bar lines */
.abcjs-clef         /* Clef */
.abcjs-key-sig      /* Key signature */
.abcjs-time-sig     /* Time signature */
.abcjs-title        /* Title */
.abcjs-rhythm       /* Rhythm notation */
.abcjs-annotation   /* Text annotations */
.abcjs-chord        /* Chord symbols */
.abcjs-lyric        /* Lyrics */
.abcjs-beam         /* Note beams */
.abcjs-slur         /* Slurs */
.abcjs-tie          /* Ties */
```

---

## Click Listener

Handle user clicks on notation:

```javascript
function clickListener(abcelem, tuneNumber, classes, analysis, drag, mouseEvent) {
  console.log('Clicked:', {
    line: analysis.line, // Zero-based line number
    measure: analysis.measure, // Measure number on line
    voice: analysis.voice, // Voice number
    name: analysis.name, // Element type ("note", etc.)
    clickedName: analysis.clickedName, // Specific clicked part
    parentClasses: analysis.parentClasses,
    selectableElement: analysis.selectableElement,
  })
}

ABCJS.renderAbc('paper', abc, {
  clickListener: clickListener,
  add_classes: true, // Required for classes info
})
```

---

## Selecting and Dragging

Enable selection and dragging of notes:

```javascript
ABCJS.renderAbc('paper', abc, {
  dragging: true,
  selectTypes: ['note'], // Or true for all types
  selectionColor: '#0066cc',
  dragColor: '#ff6600',
  clickListener: function (abcelem, tuneNumber, classes, analysis, drag) {
    if (drag && drag.step !== 0) {
      // drag.step: visual positions moved (negative = down)
      // Update ABC string and re-render
      console.log('Dragged by', drag.step, 'positions')
    }
  },
})
```

**Selectable Types:**
`"note"`, `"bar"`, `"clef"`, `"keySignature"`, `"timeSignature"`, `"title"`, `"subtitle"`, `"composer"`, `"author"`, `"tempo"`, `"part"`, `"dynamicDecoration"`, `"ending"`, `"slur"`, `"rhythm"`, `"voiceName"`, `"freeText"`, `"extraText"`, `"unalignedWords"`, `"brace"`, `"partOrder"`

---

## Tablature

Add guitar/violin tablature below standard notation:

```javascript
ABCJS.renderAbc('paper', abc, {
  tablature: [
    {
      instrument: 'guitar', // "guitar", "violin", "mandolin", "fiveString"
      label: 'Guitar (%T)', // %T = tuning
      tuning: ['E,', 'A,', 'D', 'G', 'B', 'e'], // Low to high
      capo: 0, // Fret number
      highestNote: "a'", // Highest playable note
      hideTabSymbol: false, // Hide "TAB" clef
    },
  ],
})
```

**Default Tunings:**

- Guitar: `["E,", "A,", "D", "G", "B", "e"]`
- Violin/Mandolin/Fiddle: `["G,", "D", "A", "e"]`

---

## Audio Synthesis

### CreateSynth - Low-level Audio

```javascript
const synth = new ABCJS.synth.CreateSynth()

// Must be called from user gesture (click handler)
const audioContext = new AudioContext()

await synth.init({
  visualObj: visualObj,
  audioContext: audioContext,
  millisecondsPerMeasure: visualObj.millisecondsPerMeasure(),
  options: {
    soundFontUrl: 'https://paulrosen.github.io/midi-js-soundfonts/abcjs/',
    pan: [-0.3, 0.3], // Stereo panning per track
    program: 0, // MIDI instrument (0 = piano)
    midiTranspose: 0, // Transpose MIDI output
  },
})

// Prime the audio buffer
const response = await synth.prime()
console.log('Duration:', response.duration, 'seconds')

// Playback control
synth.start()
synth.pause()
synth.resume()
synth.seek(0.5) // 50% position
synth.seek(30, 'seconds') // 30 seconds in
synth.seek(16, 'beats') // 16 beats in
synth.stop()

// Get audio data
const buffer = synth.getAudioBuffer() // AudioBuffer
const wav = synth.download() // WAV blob
```

### SynthController - UI Controls

Built-in audio control widget:

```javascript
const synthController = new ABCJS.synth.SynthController()

// Create UI in element
synthController.load('#audio-controls', cursorControl, {
  displayRestart: true,
  displayPlay: true,
  displayProgress: true,
  displayClock: true,
  displayWarp: true,
  displayLoop: true,
})

// Load tune (userAction = true if from user gesture)
synthController.setTune(visualObj, userAction, {
  qpm: 120, // Override tempo
  program: 0, // MIDI instrument
  chordsOff: false, // Disable chord playback
  voicesOff: false, // Disable voice playback
  drumIntro: 2, // Drum intro measures
  drum: 'dd 76 77 54 50 100', // Custom drum pattern
  soundFontUrl: 'https://...',
})

// Programmatic control
synthController.play()
synthController.pause()
synthController.restart()
synthController.toggleLoop()
synthController.setWarp(150) // 150% speed
synthController.download('tune.wav')
```

CSS for audio controls:

```html
<link rel="stylesheet" href="abcjs-audio.css" />
```

### MIDI File Generation

```javascript
// From visualObj
const midiBlob = ABCJS.synth.getMidiFile(visualObj, {
  midiOutputType: 'binary', // Returns Blob
})

// As download link
const linkHtml = ABCJS.synth.getMidiFile(abc, {
  midiOutputType: 'link',
  downloadLabel: 'Download MIDI for %T',
  fileName: 'tune.mid',
})

// As encoded string
const encoded = ABCJS.synth.getMidiFile(visualObj, {
  midiOutputType: 'encoded',
})
```

---

## Timing Callbacks (Animation)

Synchronize animations with music timing:

```javascript
const visualObj = ABCJS.renderAbc('paper', abc, { add_classes: true })[0]

const timingCallbacks = new ABCJS.TimingCallbacks(visualObj, {
  qpm: 120, // Tempo override
  extraMeasuresAtBeginning: 0, // Count-in measures
  beatSubdivisions: 1, // Callbacks per beat

  beatCallback: (beatNumber, totalBeats, totalTime, position, debugInfo) => {
    // Called every beat
    // position: { left, top, height } - cursor position
    console.log(`Beat ${beatNumber}/${totalBeats}`)
  },

  eventCallback: (ev) => {
    if (!ev) {
      // End of tune
      return // or return "continue" to loop
    }

    // Highlight current notes
    ev.elements.forEach((group) => {
      group.forEach((el) => el.classList.add('highlight'))
    })

    // ev properties:
    // milliseconds, millisecondsPerMeasure, line, measureNumber
    // top, height, left, width, elements
    // midiPitches: [{ pitch, durationInMeasures, volume, instrument }]
  },

  lineEndCallback: (info) => {
    // Called when reaching end of each line
    // Useful for scrolling
    console.log('Line ended:', info)
  },

  lineEndAnticipation: 500, // Call lineEndCallback 500ms early
})

// Control methods
timingCallbacks.start() // Start from beginning
timingCallbacks.start(0.5) // Start at 50%
timingCallbacks.start(10, 'seconds') // Start at 10s
timingCallbacks.start(8, 'beats') // Start at beat 8
timingCallbacks.pause()
timingCallbacks.stop()
timingCallbacks.reset()
timingCallbacks.setProgress(0.25) // Jump to 25%
timingCallbacks.replaceTarget(newVisualObj) // Change tune
```

---

## Interactive Editor

Live-updating ABC editor:

```javascript
const editor = new ABCJS.Editor('abc-textarea', {
  canvas_id: 'paper', // Render target
  warnings_id: 'warnings', // Error display
  generate_warnings: true,
  abcjsParams: {
    responsive: 'resize',
    add_classes: true,
  },

  // Audio integration
  synth: {
    el: '#audio-controls',
    cursorControl: cursorControlObject,
    options: {
      displayPlay: true,
      displayProgress: true,
    },
  },

  // Callbacks
  onchange: function () {}, // Called on ABC changes
  selectionChangeCallback: function () {}, // Called on selection change
  indicate_changed: true, // Add class when dirty
})

// Methods
editor.setReadOnly(true)
editor.paramChanged({ responsive: 'resize' }) // Update render options
editor.synthParamChanged({ qpm: 140 }) // Update synth options
editor.millisecondsPerMeasure()
editor.getTunes() // Get parsed tunes
editor.isDirty()
editor.setNotDirty()
editor.pause(true) // Pause real-time updates
```

HTML structure:

```html
<textarea id="abc-textarea">
X:1
T: My Tune
M: 4/4
K: C
CDEF|GABc|</textarea
>
<div id="warnings"></div>
<div id="paper"></div>
<div id="audio-controls"></div>
```

---

## Tune Book Analysis

Work with collections of tunes:

```javascript
// Count tunes in string
const count = ABCJS.numberOfTunes(tunebookString)

// Create TuneBook object
const tuneBook = new ABCJS.TuneBook(tunebookString)

// Access tunes
const allTunes = tuneBook.tunes // Array of tune info
const tune = tuneBook.getTuneById('1') // By X: number
const tune = tuneBook.getTuneByTitle("Cooley's")

// Extract measures
const measures = ABCJS.extractMeasures(tunebookString)

// Render specific tune from tunebook
ABCJS.renderAbc('paper', tunebookString, { startingTune: 2 })
```

---

## Transposition

```javascript
// Visual transposition (during render)
ABCJS.renderAbc('paper', abc, { visualTranspose: 5 }) // Up 5 semitones

// String transposition (returns new ABC)
const transposedAbc = ABCJS.strTranspose(abc, -3) // Down 3 semitones
```

---

## Examples

See `reference/abcjs/examples/` for complete working examples:

| File                   | Description             |
| ---------------------- | ----------------------- |
| `basic.html`           | Simple rendering        |
| `basic-synth.html`     | Audio playback          |
| `full-synth.html`      | Complete audio control  |
| `editor.html`          | Live editor             |
| `animation.html`       | Cursor and highlighting |
| `tablatures.html`      | Guitar/instrument tabs  |
| `basic-transpose.html` | Key transposition       |
| `dragging.html`        | Note editing            |
| `karaoke-synth.html`   | Karaoke-style display   |

---

## TypeScript Support

```typescript
import ABCJS, { TuneObject, SynthController, TimingCallbacks, Editor } from 'abcjs'
```

---

## Full Documentation

https://docs.abcjs.net
