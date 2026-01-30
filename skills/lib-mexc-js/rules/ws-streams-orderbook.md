---
title: WebSocket Order Book
impact: MEDIUM
impactDescription: enables accurate local order book maintenance
tags: websocket, orderbook, depth, streams
---

## WebSocket Order Book

Maintain local order book with diff depth streams.

**Correct:**

```javascript
const axios = require("axios");
const WebSocket = require("ws");

// 1. Get snapshot via REST
const snapshot = await axios.get(
  "https://api.mexc.com/api/v3/depth?symbol=BTCUSDT&limit=1000",
);

let localBook = {
  bids: new Map(snapshot.data.bids.map(([p, q]) => [p, q])),
  asks: new Map(snapshot.data.asks.map(([p, q]) => [p, q])),
  version: snapshot.data.lastUpdateId,
};

// 2. Subscribe to diff depth stream
const ws = new WebSocket("wss://wbs-api.mexc.com/ws");

ws.on("open", () => {
  ws.send(
    JSON.stringify({
      method: "SUBSCRIPTION",
      params: ["spot@public.aggre.depth.v3.api.pb@100ms@BTCUSDT"],
    }),
  );
});

// 3. Process updates
function processDepthUpdate(update) {
  // Validate version continuity
  // fromVersion should equal toVersion + 1 of previous message
  if (update.toVersion <= localBook.version) return; // Outdated, ignore

  if (update.fromVersion > localBook.version + 1) {
    // Gap detected, reinitialize from REST snapshot
    console.log("Version gap detected, reinitializing...");
    return;
  }

  // Apply bid updates
  update.bidsList.forEach(({ price, quantity }) => {
    if (parseFloat(quantity) === 0) {
      localBook.bids.delete(price);
    } else {
      localBook.bids.set(price, quantity);
    }
  });

  // Apply ask updates
  update.asksList.forEach(({ price, quantity }) => {
    if (parseFloat(quantity) === 0) {
      localBook.asks.delete(price);
    } else {
      localBook.asks.set(price, quantity);
    }
  });

  localBook.version = update.toVersion;
}
```

**Version Validation Rules:**

1. `fromVersion` should equal `toVersion + 1` of previous message
2. If `toVersion` < snapshot version, ignore (outdated)
3. If `fromVersion` > snapshot version + 1, reinitialize from REST
4. Quantity = 0 means remove that price level

Reference: [reference/websocket_market_streams.md#how-to-properly-maintain-a-local-copy-of-the-order-book](../reference/websocket_market_streams.md)
