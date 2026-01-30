# MEXC Spot API Best Practices

**Version 1.0.0**
MEXC Dev Community
January 2026

> **Note:**
> This document is for agents and LLMs to follow when maintaining, generating, or refactoring code. Contains 18 rules across 9 categories, with detailed code examples and API references.

---

## Abstract

Comprehensive guide for integrating with the MEXC Spot V3 API (REST & WebSocket). Contains 18 rules prioritized by impact from CRITICAL (Authentication) to LOW (Sub-Accounts). Key features include Protocol Buffers for WebSocket streams, HMAC-SHA256 authentication, and self-trade prevention. Each rule includes detailed explanations, incorrect vs correct implementations, and references to local documentation.

---

## Table of Contents

1. [Authentication](#1-authentication) — **CRITICAL**
   - 1.1 [Authentication & Signatures](#11-authentication--signatures)
   - 1.2 [Base Configuration](#12-base-configuration)
2. [REST API Trading](#2-rest-api-trading) — **HIGH**
   - 2.1 [REST API Trading (Orders)](#21-rest-api-trading-orders)
   - 2.2 [Batch Orders](#22-batch-orders)
3. [REST API Data](#3-rest-api-data) — **HIGH**
   - 3.1 [REST API Market Data](#31-rest-api-market-data)
   - 3.2 [REST API Account Information](#32-rest-api-account-information)
4. [WebSocket Streams](#4-websocket-streams) — **MEDIUM**
   - 4.1 [WebSocket Market Streams](#41-websocket-market-streams)
   - 4.2 [WebSocket Order Book](#42-websocket-order-book)
   - 4.3 [Protocol Buffers Integration](#43-protocol-buffers-integration)
5. [User Data Streams](#5-user-data-streams) — **MEDIUM**
   - 5.1 [User Data Streams (Account)](#51-user-data-streams-account)
   - 5.2 [User Data Streams (Orders)](#52-user-data-streams-orders)
6. [Error Handling](#6-error-handling) — **MEDIUM**
   - 6.1 [Error Handling Strategies](#61-error-handling-strategies)
   - 6.2 [Error Codes Reference](#62-error-codes-reference)
7. [Rate Limiting](#7-rate-limiting) — **LOW**
   - 7.1 [Rate Limiting](#71-rate-limiting)
   - 7.2 [WebSocket Limits](#72-websocket-limits)
8. [Wallet Operations](#8-wallet-operations) — **LOW**
   - 8.1 [Withdraw](#81-withdraw)
   - 8.2 [Deposit](#82-deposit)
9. [Sub-Accounts](#9-sub-accounts) — **LOW**
   - 9.1 [Sub-Account Management](#91-sub-account-management)

---

## 1. Authentication

**Impact: CRITICAL**

Fundamental patterns for securely accessing signed endpoints.

### 1.1 Authentication & Signatures

MEXC API endpoints require authentication using an API Key and HMAC-SHA256 signature. The signature must be lowercase hex.

**Incorrect:**

```javascript
// Sending secret key over the wire
const params = { symbol: "BTCUSDT", secret: "MY_SECRET_KEY" };

// Using wrong timestamp unit
const timestamp = Math.floor(Date.now() / 1000); // Wrong! Use milliseconds

// Uppercase signature (will fail)
const signature = crypto
  .createHmac("sha256", secret)
  .update(query)
  .digest("hex")
  .toUpperCase();
```

**Correct:**

```javascript
const crypto = require("crypto");
const axios = require("axios");

const apiKey = "YOUR_API_KEY";
const apiSecret = "YOUR_SECRET_KEY";
const baseURL = "https://api.mexc.com";

async function signedRequest(method, endpoint, params = {}) {
  const timestamp = Date.now();
  const queryString = new URLSearchParams({ ...params, timestamp }).toString();

  // Signature must be lowercase hex
  const signature = crypto
    .createHmac("sha256", apiSecret)
    .update(queryString)
    .digest("hex");

  const url = `${baseURL}${endpoint}?${queryString}&signature=${signature}`;

  return axios({
    method,
    url,
    headers: {
      "X-MEXC-APIKEY": apiKey, // Note: X-MEXC-APIKEY, not X-MBX-APIKEY
      "Content-Type": "application/json",
    },
  });
}
```

**Mixed Parameters (Query String + Body):**

```javascript
// When mixing query string and body, concatenate WITHOUT & separator
// queryString: symbol=BTCUSDT&side=BUY&type=LIMIT
// requestBody: quantity=1&price=11&recvWindow=5000&timestamp=1644489390087
// totalParams: symbol=BTCUSDT&side=BUY&type=LIMITquantity=1&price=11...
// Note: No & between "LIMIT" and "quantity"
```

**API Reference:** [reference/general_info.md#signed](reference/general_info.md)

### 1.2 Base Configuration

Configure base URLs and default settings for MEXC API.

```javascript
const config = {
  rest: "https://api.mexc.com",
  ws: "wss://wbs-api.mexc.com/ws",
  headers: {
    "X-MEXC-APIKEY": process.env.MEXC_API_KEY,
    "Content-Type": "application/json",
  },
  recvWindow: 5000, // Recommended: 5000ms or less, max: 60000ms
};
```

**Timing Security:**

```javascript
// Request validation logic on server:
// if (timestamp < serverTime + 1000 && serverTime - timestamp <= recvWindow)
//   process request
// else
//   reject request
```

---

## 2. REST API Trading

**Impact: HIGH**

Patterns for reliable order execution.

### 2.1 REST API Trading (Orders)

All trading endpoints are SIGNED and require timestamp + signature.

**Order Types & Required Parameters:**

| Type        | Required Parameters                           |
| ----------- | --------------------------------------------- |
| LIMIT       | symbol, side, type, quantity, price           |
| MARKET      | symbol, side, type, quantity OR quoteOrderQty |
| LIMIT_MAKER | symbol, side, type, quantity, price           |

**Incorrect:**

```javascript
// Missing timestamp
const params = {
  symbol: "BTCUSDT",
  side: "BUY",
  type: "LIMIT",
  quantity: 1,
  price: 50000,
};

// Using quantity for MARKET buy with quote amount
const params = {
  symbol: "BTCUSDT",
  side: "BUY",
  type: "MARKET",
  quantity: 100,
};
// This buys 100 BTC, not 100 USDT worth!
```

**Correct (Place Order):**

```javascript
async function placeOrder(symbol, side, type, options = {}) {
  const params = {
    symbol,
    side, // "BUY" or "SELL"
    type, // "LIMIT", "MARKET", "LIMIT_MAKER"
    ...options,
  };

  // For LIMIT orders, quantity and price required
  // For MARKET buy, use quoteOrderQty to specify USDT amount
  // For MARKET sell, use quantity to specify coin amount

  return signedRequest("POST", "/api/v3/order", params);
}

// Buy 100 USDT worth of BTC at market price
await placeOrder("BTCUSDT", "BUY", "MARKET", { quoteOrderQty: 100 });

// Sell 0.001 BTC at market price
await placeOrder("BTCUSDT", "SELL", "MARKET", { quantity: 0.001 });

// Place limit order with self-trade prevention
await placeOrder("BTCUSDT", "BUY", "LIMIT", {
  quantity: 0.001,
  price: 50000,
  stpMode: "cancel_taker", // "", "cancel_maker", "cancel_taker", "cancel_both"
});
```

**API Reference:** [reference/spot_account_trade.md#new-order](reference/spot_account_trade.md)

### 2.2 Batch Orders

Supports 20 orders with same symbol in a batch. Rate limit: 2 times/second.

```javascript
async function batchOrders(orders) {
  // orders is array: [{ symbol, side, type, quantity, price, ... }, ...]
  const params = {
    batchOrders: JSON.stringify(orders),
  };

  return signedRequest("POST", "/api/v3/batchOrders", params);
}

// Example batch
const orders = [
  {
    symbol: "BTCUSDT",
    side: "BUY",
    type: "LIMIT",
    quantity: "0.0002",
    price: "40000",
  },
  {
    symbol: "BTCUSDT",
    side: "SELL",
    type: "LIMIT",
    quantity: "0.0003",
    price: "45000",
  },
];
await batchOrders(orders);
```

**API Reference:** [reference/spot_account_trade.md#batch-orders](reference/spot_account_trade.md)

---

## 3. REST API Data

**Impact: HIGH**

### 3.1 REST API Market Data

Public endpoints, no authentication required.

```javascript
const axios = require("axios");
const baseURL = "https://api.mexc.com";

// Test connectivity
const ping = await axios.get(`${baseURL}/api/v3/ping`);

// Server time
const time = await axios.get(`${baseURL}/api/v3/time`);

// Exchange info (trading rules, symbol info)
const info = await axios.get(`${baseURL}/api/v3/exchangeInfo?symbol=BTCUSDT`);

// Order book (weight: 1, max limit: 5000)
const depth = await axios.get(
  `${baseURL}/api/v3/depth?symbol=BTCUSDT&limit=100`,
);

// Recent trades (weight: 5, max limit: 1000)
const trades = await axios.get(
  `${baseURL}/api/v3/trades?symbol=BTCUSDT&limit=500`,
);

// Klines/Candlesticks
const klines = await axios.get(
  `${baseURL}/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100`,
);
// Index: 0=openTime, 1=open, 2=high, 3=low, 4=close, 5=volume, 6=closeTime, 7=quoteVolume

// 24hr ticker
const ticker = await axios.get(`${baseURL}/api/v3/ticker/24hr?symbol=BTCUSDT`);
```

**API Reference:** [reference/market_data_endpoints.md](reference/market_data_endpoints.md)

### 3.2 REST API Account Information

Requires SIGNED request with `SPOT_ACCOUNT_READ` permission.

```javascript
// Account info with balances
const account = await signedRequest("GET", "/api/v3/account", {});
console.log(
  "Balances:",
  account.data.balances.filter((b) => parseFloat(b.free) > 0),
);

// Query order status
const order = await signedRequest("GET", "/api/v3/order", {
  symbol: "BTCUSDT",
  orderId: "123456789",
});

// All open orders
const openOrders = await signedRequest("GET", "/api/v3/openOrders", {
  symbol: "BTCUSDT",
});

// Trade history
const myTrades = await signedRequest("GET", "/api/v3/myTrades", {
  symbol: "BTCUSDT",
  limit: 100,
});
```

**API Reference:** [reference/spot_account_trade.md](reference/spot_account_trade.md)

---

## 4. WebSocket Streams

**Impact: MEDIUM**

### 4.1 WebSocket Market Streams

Real-time market data without authentication. Uses Protocol Buffers format.

**Connection Details:**

- Base URL: `wss://wbs-api.mexc.com/ws`
- Max 24 hours per connection
- Max 30 subscriptions per connection
- Disconnect after 30s without valid subscription
- Disconnect after 60s without data flow (send PING)

```javascript
const WebSocket = require("ws");

const ws = new WebSocket("wss://wbs-api.mexc.com/ws");

ws.on("open", () => {
  // Subscribe to trade stream (100ms aggregation)
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
});

// Keep alive with PING
setInterval(() => {
  ws.send(JSON.stringify({ method: "PING" }));
}, 30000);

ws.on("message", (data) => {
  // Data is in Protocol Buffers format - requires deserialization
  // See section 4.3 for protobuf integration
});
```

**Stream Types:**

| Stream Pattern                                                  | Description             |
| --------------------------------------------------------------- | ----------------------- |
| `spot@public.aggre.deals.v3.api.pb@(100ms\|10ms)@<symbol>`      | Trade streams           |
| `spot@public.kline.v3.api.pb@<symbol>@<interval>`               | Kline streams           |
| `spot@public.aggre.depth.v3.api.pb@(100ms\|10ms)@<symbol>`      | Diff depth              |
| `spot@public.limit.depth.v3.api.pb@<symbol>@<level>`            | Partial depth (5/10/20) |
| `spot@public.aggre.bookTicker.v3.api.pb@(100ms\|10ms)@<symbol>` | Best bid/ask            |
| `spot@public.miniTickers.v3.api.pb@<timezone>`                  | All mini tickers        |

**API Reference:** [reference/websocket_market_streams.md](reference/websocket_market_streams.md)

### 4.2 WebSocket Order Book

Maintain local order book with diff depth streams.

```javascript
// 1. Get snapshot via REST
const snapshot = await axios.get(
  `${baseURL}/api/v3/depth?symbol=BTCUSDT&limit=1000`,
);
let localBook = {
  bids: new Map(snapshot.data.bids.map(([p, q]) => [p, q])),
  asks: new Map(snapshot.data.asks.map(([p, q]) => [p, q])),
  version: snapshot.data.lastUpdateId,
};

// 2. Subscribe to diff depth
ws.send(
  JSON.stringify({
    method: "SUBSCRIPTION",
    params: ["spot@public.aggre.depth.v3.api.pb@100ms@BTCUSDT"],
  }),
);

// 3. Process updates
function processDepthUpdate(update) {
  // Validate version continuity
  // fromVersion should equal toVersion + 1 of previous message
  if (update.toVersion <= localBook.version) return; // Outdated, ignore

  // Apply updates
  update.bids.forEach(([price, qty]) => {
    if (parseFloat(qty) === 0) {
      localBook.bids.delete(price);
    } else {
      localBook.bids.set(price, qty);
    }
  });

  update.asks.forEach(([price, qty]) => {
    if (parseFloat(qty) === 0) {
      localBook.asks.delete(price);
    } else {
      localBook.asks.set(price, qty);
    }
  });

  localBook.version = update.toVersion;
}
```

**API Reference:** [reference/websocket_market_streams.md#how-to-properly-maintain-a-local-copy-of-the-order-book](reference/websocket_market_streams.md)

### 4.3 Protocol Buffers Integration

MEXC WebSocket uses Protocol Buffers format. Integration steps:

**1. Get Proto Files:**

```bash
git clone https://github.com/mexcdevelop/websocket-proto
```

**2. Generate Deserialization Code:**

```bash
# For Node.js
protoc --js_out=import_style=commonjs,binary:. *.proto

# For Python
protoc *.proto --python_out=./
```

**3. Deserialize in JavaScript:**

```javascript
const protobuf = require("protobufjs");

// Load proto definition
const root = await protobuf.load("./PushDataV3ApiWrapper.proto");
const PushDataWrapper = root.lookupType("PushDataV3ApiWrapper");

ws.on("message", (buffer) => {
  // Decode protobuf message
  const message = PushDataWrapper.decode(buffer);
  const data = PushDataWrapper.toObject(message);

  console.log("Channel:", data.channel);
  console.log("Symbol:", data.symbol);
  console.log(
    "Payload:",
    data.publicDeals || data.publicSpotkline || data.publicIncreasedepths,
  );
});
```

**API Reference:** [reference/websocket_market_streams.md#protocol-buffers-integration](reference/websocket_market_streams.md)

---

## 5. User Data Streams

**Impact: MEDIUM**

### 5.1 User Data Streams (Account)

Real-time balance and position updates.

```javascript
// 1. Create listen key (valid for 60 minutes)
const {
  data: { listenKey },
} = await axios.post(`${baseURL}/api/v3/userDataStream`, null, {
  headers: { "X-MEXC-APIKEY": apiKey },
});

// 2. Connect with listen key
const ws = new WebSocket(`wss://wbs-api.mexc.com/ws?listenKey=${listenKey}`);

// 3. Subscribe to account updates
ws.on("open", () => {
  ws.send(
    JSON.stringify({
      method: "SUBSCRIPTION",
      params: ["spot@private.account.v3.api.pb"],
    }),
  );
});

// 4. Handle account updates
ws.on("message", (data) => {
  const event = JSON.parse(data);
  if (event.channel === "spot@private.account.v3.api.pb") {
    const account = event.privateAccount;
    console.log("Asset:", account.vcoinName);
    console.log("Balance:", account.balanceAmount);
    console.log("Change:", account.balanceAmountChange);
    console.log("Type:", account.type); // e.g., "CONTRACT_TRANSFER"
  }
});

// 5. Keep alive every 30 minutes (extends validity to 60 min)
setInterval(
  () => {
    axios.put(`${baseURL}/api/v3/userDataStream?listenKey=${listenKey}`, null, {
      headers: { "X-MEXC-APIKEY": apiKey },
    });
  },
  30 * 60 * 1000,
);
```

**API Reference:** [reference/websocket_user_data_streams.md](reference/websocket_user_data_streams.md)

### 5.2 User Data Streams (Orders)

Order updates via private streams.

```javascript
// Subscribe to order updates
ws.send(
  JSON.stringify({
    method: "SUBSCRIPTION",
    params: ["spot@private.orders.v3.api.pb"],
  }),
);

// Subscribe to deal updates
ws.send(
  JSON.stringify({
    method: "SUBSCRIPTION",
    params: ["spot@private.deals.v3.api.pb"],
  }),
);

ws.on("message", (data) => {
  const event = JSON.parse(data);

  if (event.channel === "spot@private.orders.v3.api.pb") {
    const order = event.privateOrders;
    console.log("Order ID:", order.clientId);
    console.log("Status:", order.status);
    // Status: 1=Not traded, 2=Fully traded, 3=Partially traded, 4=Canceled, 5=Partially canceled
    console.log("Type:", order.orderType);
    // orderType: 1=LIMIT, 2=POST_ONLY, 3=IOC, 4=FOK, 5=MARKET, 100=Stop
    console.log("Cumulative Qty:", order.cumulativeQuantity);
    console.log("Cumulative Amount:", order.cumulativeAmount);
  }

  if (event.channel === "spot@private.deals.v3.api.pb") {
    const deal = event.privateDeals;
    console.log("Trade ID:", deal.tradeId);
    console.log("Price:", deal.price);
    console.log("Quantity:", deal.quantity);
    console.log("Is Maker:", deal.isMaker);
    console.log("Fee:", deal.feeAmount, deal.feeCurrency);
  }
});
```

---

## 6. Error Handling

**Impact: MEDIUM**

### 6.1 Error Handling Strategies

**HTTP Return Codes:**

| Code | Description         | Action                         |
| ---- | ------------------- | ------------------------------ |
| 4XX  | Malformed request   | Fix request parameters         |
| 403  | WAF limit violated  | Check request rate             |
| 429  | Rate limit exceeded | Back off, respect Retry-After  |
| 5XX  | Server error        | Retry with exponential backoff |

**Correct Error Handling:**

```javascript
async function safeRequest(method, endpoint, params) {
  try {
    return await signedRequest(method, endpoint, params);
  } catch (error) {
    const status = error.response?.status;
    const code = error.response?.data?.code;

    if (status === 429) {
      const retryAfter = error.response.headers["retry-after"] || 60;
      console.log(`Rate limited. Retry after ${retryAfter}s`);
      await sleep(retryAfter * 1000);
      return safeRequest(method, endpoint, params);
    }

    if (status >= 500) {
      console.log("Server error, retrying...");
      await sleep(1000);
      return safeRequest(method, endpoint, params);
    }

    // Handle specific error codes
    switch (code) {
      case 700003:
        console.log("Timestamp outside recvWindow, sync clock");
        break;
      case 700002:
        console.log("Invalid signature");
        break;
      case 30004:
        console.log("Insufficient balance");
        break;
      default:
        console.log(`Error ${code}: ${error.response?.data?.msg}`);
    }

    throw error;
  }
}
```

### 6.2 Error Codes Reference

**Critical Error Codes:**

| Code   | Description                   |
| ------ | ----------------------------- |
| 400    | API key required              |
| 602    | Signature verification failed |
| 700002 | Signature not valid           |
| 700003 | Timestamp outside recvWindow  |
| 700005 | recvWindow must be < 60000    |
| 30004  | Insufficient position/balance |
| 30014  | Invalid symbol                |
| 30016  | Trading disabled              |
| 30018  | Market order disabled         |
| 30029  | Cannot exceed max order limit |
| 10101  | Insufficient balance          |

**API Reference:** [reference/general_info.md#error-code](reference/general_info.md)

---

## 7. Rate Limiting

**Impact: LOW**

### 7.1 Rate Limiting

**Limits:**

- IP limit: 500 requests per 10 seconds per endpoint
- UID limit: 500 requests per 10 seconds per endpoint
- Each endpoint has independent limits

**Best Practices:**

```javascript
class RateLimiter {
  constructor(limit = 500, window = 10000) {
    this.limit = limit;
    this.window = window;
    this.requests = [];
  }

  async throttle() {
    const now = Date.now();
    this.requests = this.requests.filter((t) => now - t < this.window);

    if (this.requests.length >= this.limit) {
      const waitTime = this.window - (now - this.requests[0]);
      await sleep(waitTime);
    }

    this.requests.push(Date.now());
  }
}

const limiter = new RateLimiter();

async function rateLimitedRequest(method, endpoint, params) {
  await limiter.throttle();
  return signedRequest(method, endpoint, params);
}
```

### 7.2 WebSocket Limits

- Connection rate: 100 times/second
- Max subscriptions per connection: 30
- Connection exceeding limit will be disconnected
- IPs repeatedly disconnected may be banned

---

## 8. Wallet Operations

**Impact: LOW**

### 8.1 Withdraw

Requires `SPOT_WITHDRAW_WRITE` permission.

```javascript
// Get available networks for a coin
const config = await signedRequest("GET", "/api/v3/capital/config/getall", {});
const btcNetworks = config.data.find((c) => c.coin === "BTC").networkList;

// Withdraw
const withdraw = await signedRequest("POST", "/api/v3/capital/withdraw", {
  coin: "USDT",
  address: "TRx123...",
  amount: "100",
  netWork: "TRC20", // Use netWork from config
});
console.log("Withdraw ID:", withdraw.data.id);

// Cancel withdraw
await signedRequest("DELETE", "/api/v3/capital/withdraw", {
  id: withdraw.data.id,
});
```

### 8.2 Deposit

```javascript
// Generate deposit address
const address = await signedRequest("POST", "/api/v3/capital/deposit/address", {
  coin: "USDT",
  network: "TRC20",
});
console.log("Address:", address.data.address);
console.log("Memo:", address.data.memo);

// Get deposit history
const history = await signedRequest("GET", "/api/v3/capital/deposit/hisrec", {
  coin: "USDT",
  limit: 100,
});
// Status: 1=Small, 2=Medium, 3=Large, 4=SuperLarge, 5=Success
```

**API Reference:** [reference/wallet_endpoints.md](reference/wallet_endpoints.md)

---

## 9. Sub-Accounts

**Impact: LOW**

### 9.1 Sub-Account Management

Only master account API key can access these endpoints.

```javascript
// Create sub-account
const subAccount = await signedRequest(
  "POST",
  "/api/v3/sub-account/virtualSubAccount",
  {
    subAccount: "trading_bot_1",
    note: "Automated trading bot",
  },
);

// List sub-accounts
const list = await signedRequest("GET", "/api/v3/sub-account/list", {});

// Create API key for sub-account
const apiKey = await signedRequest("POST", "/api/v3/sub-account/apiKey", {
  subAccount: "trading_bot_1",
  note: "Trading API",
  permissions: "SPOT_DEAL_READ,SPOT_DEAL_WRITE",
  ip: "1.2.3.4", // Optional, up to 20 IPs
});

// Transfer between accounts
const transfer = await signedRequest(
  "POST",
  "/api/v3/capital/sub-account/universalTransfer",
  {
    toAccount: "trading_bot_1",
    fromAccountType: "SPOT",
    toAccountType: "SPOT",
    asset: "USDT",
    amount: "1000",
  },
);
```

**API Reference:** [reference/sub*account_endpoints_only_supports_main_account_api_key*.md](reference/sub_account_endpoints_only_supports_main_account_api_key_.md)

---

## References

1. [General API Info](reference/general_info.md)
2. [Market Data Endpoints](reference/market_data_endpoints.md)
3. [Spot Account/Trade](reference/spot_account_trade.md)
4. [WebSocket Market Streams](reference/websocket_market_streams.md)
5. [WebSocket User Data Streams](reference/websocket_user_data_streams.md)
6. [Wallet Endpoints](reference/wallet_endpoints.md)
7. [Sub-Account Endpoints](reference/sub_account_endpoints_only_supports_main_account_api_key_.md)
8. [MEXC API Documentation](https://www.mexc.com/api-docs)
9. [WebSocket Proto Files](https://github.com/mexcdevelop/websocket-proto)
