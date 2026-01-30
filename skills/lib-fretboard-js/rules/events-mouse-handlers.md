---
title: Add Mouse Event Handlers
impact: MEDIUM
impactDescription: enables interactive applications
tags: events, click, mousemove, on, handlers
---

## Add Mouse Event Handlers

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
