---
title: Sub-Account Management
impact: LOW
impactDescription: enables multi-account trading strategies
tags: sub-account, api-key, transfer
---

## Sub-Account Management

Create and manage sub-accounts. Only master account API key can access these endpoints.

**Correct:**

```javascript
// 1. Create sub-account
const subAccount = await signedRequest(
  "POST",
  "/api/v3/sub-account/virtualSubAccount",
  {
    subAccount: "trading_bot_1", // 8-32 alphanumeric characters
    note: "Automated trading bot",
  },
);

// 2. List sub-accounts
const list = await signedRequest("GET", "/api/v3/sub-account/list", {
  page: 1,
  limit: 100, // Max 200
});
list.data.subAccounts.forEach((sub) => {
  console.log("Name:", sub.subAccount);
  console.log("UID:", sub.uid);
  console.log("Frozen:", sub.isFreeze);
  console.log("Created:", sub.createTime);
});

// 3. Create API key for sub-account
const apiKey = await signedRequest("POST", "/api/v3/sub-account/apiKey", {
  subAccount: "trading_bot_1",
  note: "Trading API",
  permissions: "SPOT_DEAL_READ,SPOT_DEAL_WRITE", // Comma-separated
  ip: "1.2.3.4,5.6.7.8", // Optional, up to 20 IPs
});
console.log("API Key:", apiKey.data.apiKey);
console.log("Secret Key:", apiKey.data.secretKey);

// 4. Query sub-account API keys
const keys = await signedRequest("GET", "/api/v3/sub-account/apiKey", {
  subAccount: "trading_bot_1",
});

// 5. Delete sub-account API key
await signedRequest("DELETE", "/api/v3/sub-account/apiKey", {
  subAccount: "trading_bot_1",
  apiKey: "mx0...",
});

// 6. Transfer between accounts
const transfer = await signedRequest(
  "POST",
  "/api/v3/capital/sub-account/universalTransfer",
  {
    toAccount: "trading_bot_1", // Omit for master account
    fromAccountType: "SPOT",
    toAccountType: "SPOT",
    asset: "USDT",
    amount: "1000",
  },
);
console.log("Transfer ID:", transfer.data.tranId);

// 7. Query sub-account balances
const balances = await signedRequest("GET", "/api/v3/sub-account/asset", {
  subAccount: "trading_bot_1",
  accountType: "SPOT", // Currently only SPOT supported
});
```

**Available Permissions:**

| Permission             | Description            |
| ---------------------- | ---------------------- |
| SPOT_ACCOUNT_READ      | Read spot account      |
| SPOT_ACCOUNT_WRITE     | Write spot account     |
| SPOT_DEAL_READ         | Read spot trades       |
| SPOT_DEAL_WRITE        | Execute spot trades    |
| CONTRACT_ACCOUNT_READ  | Read futures account   |
| CONTRACT_ACCOUNT_WRITE | Write futures account  |
| CONTRACT_DEAL_READ     | Read futures trades    |
| CONTRACT_DEAL_WRITE    | Execute futures trades |
| SPOT_TRANSFER_READ     | Read transfers         |
| SPOT_TRANSFER_WRITE    | Execute transfers      |

Reference: [reference/sub*account_endpoints_only_supports_main_account_api_key*.md](../reference/sub_account_endpoints_only_supports_main_account_api_key_.md)
