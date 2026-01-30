---
title: Batch Orders
impact: HIGH
impactDescription: efficient multi-order placement in single request
tags: batch-orders, trading, rest-api, bulk
---

## Batch Orders

Supports 20 orders with same symbol in a batch. Rate limit: 2 times/second.

**Incorrect:**

```javascript
// Exceeding batch limit
const orders = Array(25).fill({ symbol: "BTCUSDT", ... }); // Max is 20!

// Mixed symbols in batch
const orders = [
  { symbol: "BTCUSDT", ... },
  { symbol: "ETHUSDT", ... }, // Different symbol not allowed!
];
```

**Correct:**

```javascript
async function batchOrders(orders) {
  // All orders must have the same symbol
  const params = {
    batchOrders: JSON.stringify(orders),
  };
  return signedRequest("POST", "/api/v3/batchOrders", params);
}

// Example batch (single symbol, max 20 orders)
const orders = [
  {
    symbol: "BTCUSDT",
    side: "BUY",
    type: "LIMIT",
    quantity: "0.0002",
    price: "40000",
    newClientOrderId: "order_1",
  },
  {
    symbol: "BTCUSDT",
    side: "SELL",
    type: "LIMIT",
    quantity: "0.0003",
    price: "45000",
    newClientOrderId: "order_2",
  },
];

const result = await batchOrders(orders);
// Response includes both successful orders and errors
// Successful: { symbol, orderId, orderListId }
// Error: { newClientOrderId, msg, code }
```

**Note:** Rate limit is 2 batch requests per second.

Reference: [reference/spot_account_trade.md#batch-orders](../reference/spot_account_trade.md)
