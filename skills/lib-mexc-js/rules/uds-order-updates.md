---
title: User Data Streams Order Updates
impact: MEDIUM
impactDescription: enables real-time order and trade tracking
tags: user-data, orders, trades, execution
---

## User Data Streams Order Updates

Order updates and trade executions via private streams.

**Correct:**

```javascript
// Subscribe to order updates
ws.send(
  JSON.stringify({
    method: "SUBSCRIPTION",
    params: ["spot@private.orders.v3.api.pb"],
  }),
);

// Subscribe to deal (trade) updates
ws.send(
  JSON.stringify({
    method: "SUBSCRIPTION",
    params: ["spot@private.deals.v3.api.pb"],
  }),
);

ws.on("message", (data) => {
  const event = JSON.parse(data);

  // Order status updates
  if (event.channel === "spot@private.orders.v3.api.pb") {
    const order = event.privateOrders;
    console.log("Order ID:", order.clientId);
    console.log("Price:", order.price);
    console.log("Quantity:", order.quantity);
    console.log("Avg Price:", order.avgPrice);
    console.log("Status:", order.status);
    console.log("Order Type:", order.orderType);
    console.log("Trade Type:", order.tradeType); // 1=Buy, 2=Sell
    console.log("Remaining Qty:", order.remainQuantity);
    console.log("Cumulative Qty:", order.cumulativeQuantity);
    console.log("Cumulative Amount:", order.cumulativeAmount);
    console.log("Created:", order.createTime);
  }

  // Trade execution updates
  if (event.channel === "spot@private.deals.v3.api.pb") {
    const deal = event.privateDeals;
    console.log("Trade ID:", deal.tradeId);
    console.log("Order ID:", deal.orderId);
    console.log("Price:", deal.price);
    console.log("Quantity:", deal.quantity);
    console.log("Amount:", deal.amount);
    console.log("Trade Type:", deal.tradeType); // 1=Buy, 2=Sell
    console.log("Is Maker:", deal.isMaker);
    console.log("Fee Amount:", deal.feeAmount);
    console.log("Fee Currency:", deal.feeCurrency);
    console.log("Time:", deal.time);
  }
});
```

**Order Status Values:**

| Status | Description        |
| ------ | ------------------ |
| 1      | Not traded         |
| 2      | Fully traded       |
| 3      | Partially traded   |
| 4      | Canceled           |
| 5      | Partially canceled |

**Order Type Values:**

| Type | Description           |
| ---- | --------------------- |
| 1    | LIMIT_ORDER           |
| 2    | POST_ONLY             |
| 3    | IMMEDIATE_OR_CANCEL   |
| 4    | FILL_OR_KILL          |
| 5    | MARKET_ORDER          |
| 100  | Stop loss/take profit |

Reference: [reference/websocket_user_data_streams.md](../reference/websocket_user_data_streams.md)
