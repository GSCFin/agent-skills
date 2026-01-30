---
title: WebSocket Market Streams
impact: MEDIUM
impactDescription: enables real-time market data with low latency
tags: websocket, streams, market-data, real-time
---

## WebSocket Market Streams

Real-time market data without authentication. Uses Protocol Buffers format.

**Connection Details:**

- Base URL: `wss://wbs-api.mexc.com/ws`
- Max 24 hours per connection
- Max 30 subscriptions per connection
- Disconnect after 30s without valid subscription
- Disconnect after 60s without data flow (send PING)
- Symbols must be UPPERCASE

**Correct:**

```javascript
const WebSocket = require("ws");

const ws = new WebSocket("wss://wbs-api.mexc.com/ws");

ws.on("open", () => {
  // Subscribe to trade stream (100ms or 10ms aggregation)
  ws.send(
    JSON.stringify({
      method: "SUBSCRIPTION",
      params: ["spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT"],
    }),
  );

  // Subscribe to kline stream
  ws.send(
    JSON.stringify({
      method: "SUBSCRIPTION",
      params: ["spot@public.kline.v3.api.pb@BTCUSDT@Min15"],
    }),
  );

  // Subscribe to best bid/ask
  ws.send(
    JSON.stringify({
      method: "SUBSCRIPTION",
      params: ["spot@public.aggre.bookTicker.v3.api.pb@100ms@BTCUSDT"],
    }),
  );
});

// Keep alive with PING every 30 seconds
setInterval(() => {
  ws.send(JSON.stringify({ method: "PING" }));
}, 30000);

// Unsubscribe
ws.send(
  JSON.stringify({
    method: "UNSUBSCRIPTION",
    params: ["spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT"],
  }),
);
```

**Stream Pattern Reference:**

| Pattern                                                         | Description             |
| --------------------------------------------------------------- | ----------------------- |
| `spot@public.aggre.deals.v3.api.pb@(100ms\|10ms)@<symbol>`      | Trade streams           |
| `spot@public.kline.v3.api.pb@<symbol>@<interval>`               | Kline streams           |
| `spot@public.aggre.depth.v3.api.pb@(100ms\|10ms)@<symbol>`      | Diff depth              |
| `spot@public.limit.depth.v3.api.pb@<symbol>@<level>`            | Partial depth (5/10/20) |
| `spot@public.aggre.bookTicker.v3.api.pb@(100ms\|10ms)@<symbol>` | Best bid/ask            |
| `spot@public.miniTickers.v3.api.pb@<timezone>`                  | All mini tickers        |

**Kline Intervals:** Min1, Min5, Min15, Min30, Min60, Hour4, Hour8, Day1, Week1, Month1

Reference: [reference/websocket_market_streams.md](../reference/websocket_market_streams.md)
