---
title: REST API Market Data
impact: HIGH
impactDescription: essential for informed trading decisions
tags: market-data, rest-api, orderbook, trades, klines
---

## REST API Market Data

Public endpoints, no authentication required.

**Correct:**

```javascript
const axios = require("axios");
const baseURL = "https://api.mexc.com";

// Test connectivity
const ping = await axios.get(`${baseURL}/api/v3/ping`);
// Response: {}

// Server time
const time = await axios.get(`${baseURL}/api/v3/time`);
// Response: { serverTime: 1645539742000 }

// Exchange info (trading rules, symbol info)
const info = await axios.get(`${baseURL}/api/v3/exchangeInfo?symbol=BTCUSDT`);
// Includes: status, baseAsset, quoteAsset, orderTypes, filters

// Order book (weight: 1, max limit: 5000)
const depth = await axios.get(
  `${baseURL}/api/v3/depth?symbol=BTCUSDT&limit=100`,
);
// Response: { lastUpdateId, bids: [[price, qty]], asks: [[price, qty]] }

// Recent trades (weight: 5, max limit: 1000)
const trades = await axios.get(
  `${baseURL}/api/v3/trades?symbol=BTCUSDT&limit=500`,
);

// Klines/Candlesticks
const klines = await axios.get(
  `${baseURL}/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100`,
);
// Index: 0=openTime, 1=open, 2=high, 3=low, 4=close, 5=volume, 6=closeTime, 7=quoteVolume

// 24hr ticker (weight: 1 for single, 40 for all)
const ticker = await axios.get(`${baseURL}/api/v3/ticker/24hr?symbol=BTCUSDT`);

// Average price
const avgPrice = await axios.get(`${baseURL}/api/v3/avgPrice?symbol=BTCUSDT`);
```

**Kline Intervals:** 1m, 5m, 15m, 30m, 60m, 4h, 8h, 1d, 1w, 1M

Reference: [reference/market_data_endpoints.md](../reference/market_data_endpoints.md)
