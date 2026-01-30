---
title: Error Codes Reference
impact: MEDIUM
impactDescription: enables accurate error diagnosis and handling
tags: errors, codes, debugging, api
---

## Error Codes Reference

Complete reference of MEXC API error codes.

**Authentication Errors:**

| Code   | Description                   |
| ------ | ----------------------------- |
| 400    | API key required              |
| 602    | Signature verification failed |
| 700001 | API-key format invalid        |
| 700002 | Signature not valid           |
| 700003 | Timestamp outside recvWindow  |
| 700005 | recvWindow must be < 60000    |
| 700006 | IP not in whitelist           |
| 700007 | No permission for endpoint    |

**Trading Errors:**

| Code  | Description                  |
| ----- | ---------------------------- |
| -2011 | Unknown order sent           |
| 30000 | Trading suspended for symbol |
| 30001 | Direction not allowed        |
| 30002 | Min quantity not met         |
| 30003 | Max quantity exceeded        |
| 30004 | Insufficient balance         |
| 30010 | No valid trade price         |
| 30014 | Invalid symbol               |
| 30016 | Trading disabled             |
| 30018 | Market order disabled        |
| 30019 | API market order disabled    |
| 30026 | Invalid order IDs            |
| 30029 | Max order limit exceeded     |
| 30032 | Max position exceeded        |

**Account Errors:**

| Code  | Description              |
| ----- | ------------------------ |
| 10001 | User does not exist      |
| 10072 | Invalid access key       |
| 10073 | Invalid Request-Time     |
| 10101 | Insufficient balance     |
| 60005 | Account abnormal         |
| 70011 | User banned from trading |

**Handling Common Errors:**

```javascript
function handleError(code, msg) {
  switch (code) {
    case 700003:
      console.log("Sync your system clock");
      break;
    case 700002:
      console.log("Check signature algorithm");
      break;
    case 30004:
    case 10101:
      console.log("Insufficient balance");
      break;
    case 30014:
      console.log("Check symbol format (e.g., BTCUSDT)");
      break;
    case 30016:
    case 30018:
      console.log("Trading disabled for this pair");
      break;
    default:
      console.log(`Error ${code}: ${msg}`);
  }
}
```

Reference: [reference/general_info.md#error-code](../reference/general_info.md)
