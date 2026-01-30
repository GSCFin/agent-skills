---
name: lib-fretboard-js
description: Guitar/bass fretboard SVG visualization using fretboard.js library. Covers chord diagrams, scale patterns (CAGED, TNPS, pentatonic systems), event handling, and styling. Triggers on tasks involving guitar fretboard visualization, chord diagrams, scale boxes, tab rendering, or music theory visualization for stringed instruments.
license: ISC
metadata:
  author: moonwave99
  version: "1.0.0"
---

# fretboard.js Library Guide

Comprehensive guide for the fretboard.js library - a guitar/bass fretboard SVG visualization toolkit with music-oriented tools including scale boxes, arpeggios, chord shapes, and interactive API.

## When to Apply

Reference these guidelines when:

- Creating guitar/bass fretboard visualizations
- Rendering chord diagrams with barres and fingerings
- Displaying scale patterns using CAGED, TNPS, or pentatonic systems
- Adding interactive features (click, hover) to fretboard diagrams
- Styling fretboard dots, highlighting scale positions
- Integrating fretboard visualization with music notation (ABCJS)

## Rule Categories by Priority

| Priority | Category        | Impact   | Prefix                         |
| -------- | --------------- | -------- | ------------------------------ |
| 1        | Setup           | CRITICAL | `setup-`                       |
| 2        | Chord Rendering | HIGH     | `chords-`                      |
| 3        | Scale Rendering | HIGH     | `scales-`                      |
| 4        | Styling         | MEDIUM   | `styling-`                     |
| 5        | Events          | MEDIUM   | `events-`                      |
| 6        | Advanced        | LOW      | `tetrachords-`, `integration-` |

## Quick Reference

### 1. Setup (CRITICAL)

- `setup-installation` - Install and import fretboard.js with dependencies
- `setup-basic-fretboard` - Create basic fretboard with configuration options

### 2. Chord Rendering (HIGH)

- `chords-render-chord` - Render chord diagrams with renderChord()
- `chords-barres` - Add barre indicators to chord diagrams
- `chords-muted-strings` - Show muted/open strings with X and O markers

### 3. Scale Rendering (HIGH)

- `scales-render-scale` - Display full scale patterns with renderScale()
- `scales-systems` - Use CAGED, TNPS, or pentatonic box systems
- `scales-box-positions` - Render specific scale box positions

### 4. Styling (MEDIUM)

- `styling-dots` - Customize dot colors, text, and appearance
- `styling-highlight-areas` - Highlight rectangular fretboard regions

### 5. Events (MEDIUM)

- `events-mouse-handlers` - Add click, hover, and mouse event handlers
- `events-position-tracking` - Get note/position info from interactions

### 6. Advanced (LOW)

- `tetrachords-patterns` - Generate tetrachord patterns for scale building
- `integration-abcjs` - Sync fretboard with ABCJS notation playback

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/setup-installation.md
rules/chords-render-chord.md
rules/scales-systems.md
```

Each rule file contains:

- Brief explanation with use cases
- Incorrect code example (common mistakes)
- Correct code example with comments
- API reference and configuration options

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
