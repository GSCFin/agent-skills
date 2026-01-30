---
title: Install and Import fretboard.js
impact: CRITICAL
impactDescription: required for any fretboard visualization
tags: setup, installation, import, npm, esm
---

## Install and Import fretboard.js

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
