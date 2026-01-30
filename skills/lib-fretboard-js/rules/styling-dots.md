---
title: Customize Dot Appearance
impact: MEDIUM
impactDescription: improves visual clarity and information
tags: styling, dots, dotFill, dotText, style
---

## Customize Dot Appearance

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
