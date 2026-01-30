---
title: REST API Account Information
impact: HIGH
impactDescription: required for balance and trade history access
tags: account, balances, trades, orders, rest-api
---

## REST API Account Information

Requires SIGNED request with `SPOT_ACCOUNT_READ` permission.

**Correct:**

```javascript
// Account info with balances
const account = await signedRequest("GET", "/api/v3/account", {});
console.log(
  "Balances:",
  account.data.balances.filter((b) => parseFloat(b.free) > 0),
);

// Query UID
const uid = await signedRequest("GET", "/api/v3/uid", {});
console.log("User ID:", uid.data.uid);

// Query KYC status
const kyc = await signedRequest("GET", "/api/v3/kyc/status", {});
// Status: 1=Unverified, 2=Primary, 3=Advanced, 4=Institutional

// Query order status
const order = await signedRequest("GET", "/api/v3/order", {
  symbol: "BTCUSDT",
  orderId: "123456789", // or origClientOrderId
});

// All open orders (single symbol or all)
const openOrders = await signedRequest("GET", "/api/v3/openOrders", {
  symbol: "BTCUSDT", // Optional
});

// All orders (completed and open)
const allOrders = await signedRequest("GET", "/api/v3/allOrders", {
  symbol: "BTCUSDT",
  limit: 500, // Default 500, max 1000
});

// Trade history
const myTrades = await signedRequest("GET", "/api/v3/myTrades", {
  symbol: "BTCUSDT",
  limit: 500, // Default 500, max 1000
});
```

**Order Status Values:**

| Status           | Description        |
| ---------------- | ------------------ |
| NEW              | Order accepted     |
| PARTIALLY_FILLED | Partially executed |
| FILLED           | Fully executed     |
| CANCELED         | Canceled by user   |
| PENDING_CANCEL   | Cancel in progress |
| REJECTED         | Order rejected     |
| EXPIRED          | Order expired      |

Reference: [reference/spot_account_trade.md](../reference/spot_account_trade.md)
