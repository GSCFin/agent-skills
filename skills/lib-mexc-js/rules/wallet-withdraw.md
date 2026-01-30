---
title: Withdraw
impact: LOW
impactDescription: enables programmatic asset withdrawal
tags: wallet, withdraw, transfer
---

## Withdraw

Withdraw assets to external addresses. Requires `SPOT_WITHDRAW_WRITE` permission.

**Correct:**

```javascript
// 1. Get available networks for a coin
const config = await signedRequest("GET", "/api/v3/capital/config/getall", {});
const btcConfig = config.data.find((c) => c.coin === "BTC");
console.log(
  "Available networks:",
  btcConfig.networkList.map((n) => n.netWork),
);
// Output: ["BTC", "BSC", ...]

// 2. Check network details before withdrawing
const trc20 = btcConfig.networkList.find((n) => n.netWork === "TRC20");
console.log("Enabled:", trc20.withdrawEnable);
console.log("Fee:", trc20.withdrawFee);
console.log("Min:", trc20.withdrawMin);
console.log("Max:", trc20.withdrawMax);

// 3. Withdraw
const withdraw = await signedRequest("POST", "/api/v3/capital/withdraw", {
  coin: "USDT",
  address: "TRx123...",
  amount: "100",
  netWork: "TRC20", // Use netWork from config!
  memo: "", // Required for some chains (EOS, XRP, etc.)
  remark: "Withdrawal to cold wallet", // Optional
});
console.log("Withdraw ID:", withdraw.data.id);

// 4. Cancel withdraw (if still pending)
await signedRequest("DELETE", "/api/v3/capital/withdraw", {
  id: withdraw.data.id,
});

// 5. Get withdraw history
const history = await signedRequest("GET", "/api/v3/capital/withdraw/history", {
  coin: "USDT",
  limit: 100,
});
// Status: 1=Submitted, 2=Cancelled, 3=Failed, 4=Processing,
//         5=Email Sent, 6=Approved, 7=Completed
```

**Note:** The `netWork` field is obtained from `/api/v3/capital/config/getall` response.

Reference: [reference/wallet_endpoints.md](../reference/wallet_endpoints.md)
