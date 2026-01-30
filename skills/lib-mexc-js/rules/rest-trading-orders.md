---
title: REST API Trading Orders
impact: HIGH
impactDescription: enables reliable order placement and management
tags: orders, trading, rest-api, limit, market
---

## REST API Trading Orders

Place, query, and cancel orders via REST API. All trading endpoints are SIGNED.

**Order Types & Required Parameters:**

| Type        | Required Parameters                           |
| ----------- | --------------------------------------------- |
| LIMIT       | symbol, side, type, quantity, price           |
| MARKET      | symbol, side, type, quantity OR quoteOrderQty |
| LIMIT_MAKER | symbol, side, type, quantity, price           |

**Incorrect:**

```javascript
// Missing timestamp (will fail)
const params = {
  symbol: "BTCUSDT",
  side: "BUY",
  type: "LIMIT",
  quantity: 1,
  price: 50000,
};

// Using quantity for MARKET buy when you want to spend USDT
const params = {
  symbol: "BTCUSDT",
  side: "BUY",
  type: "MARKET",
  quantity: 100,
};
// This buys 100 BTC, not 100 USDT worth!
```

**Correct:**

```javascript
async function placeOrder(symbol, side, type, options = {}) {
  const params = {
    symbol,
    side, // "BUY" or "SELL"
    type, // "LIMIT", "MARKET", "LIMIT_MAKER"
    ...options,
  };
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

**Cancel Order:**

```javascript
await signedRequest("DELETE", "/api/v3/order", {
  symbol: "BTCUSDT",
  orderId: "123456789", // or origClientOrderId
});
```

Reference: [reference/spot_account_trade.md#new-order](../reference/spot_account_trade.md)
