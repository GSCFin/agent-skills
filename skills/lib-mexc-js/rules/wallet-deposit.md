---
title: Deposit
impact: LOW
impactDescription: enables programmatic deposit address management
tags: wallet, deposit, address
---

## Deposit

Generate and query deposit addresses.

**Correct:**

```javascript
// 1. Get existing deposit addresses
const addresses = await signedRequest(
  "GET",
  "/api/v3/capital/deposit/address",
  {
    coin: "USDT",
    network: "TRC20", // Optional
  },
);
// Returns array: [{ coin, network, address, memo }]

// 2. Generate new deposit address (if none exists)
const newAddress = await signedRequest(
  "POST",
  "/api/v3/capital/deposit/address",
  {
    coin: "USDT",
    network: "TRC20",
  },
);
console.log("Address:", newAddress.data.address);
console.log("Memo:", newAddress.data.memo); // Some chains require memo

// 3. Get deposit history
const history = await signedRequest("GET", "/api/v3/capital/deposit/hisrec", {
  coin: "USDT",
  startTime: Date.now() - 7 * 24 * 60 * 60 * 1000, // 7 days ago
  endTime: Date.now(),
  limit: 1000, // Max 1000
});

history.data.forEach((deposit) => {
  console.log("Amount:", deposit.amount);
  console.log("Coin:", deposit.coin);
  console.log("Network:", deposit.network);
  console.log("Status:", deposit.status);
  console.log("Address:", deposit.address);
  console.log("TxID:", deposit.txId);
  console.log(
    "Confirmations:",
    deposit.confirmTimes,
    "/",
    deposit.unlockConfirm,
  );
});
```

**Deposit Status Values:**

| Status | Description         |
| ------ | ------------------- |
| 1      | Small deposit       |
| 2      | Medium deposit      |
| 3      | Large deposit       |
| 4      | Super large deposit |
| 5      | Success             |

**Notes:**

- Default history returns records from last 7 days
- Can query up to 90 days of history
- Some coins require memo (EOS, XRP, ATOM, etc.)

Reference: [reference/wallet_endpoints.md](../reference/wallet_endpoints.md)
