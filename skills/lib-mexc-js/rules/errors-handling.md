---
title: Error Handling Strategies
impact: MEDIUM
impactDescription: prevents cascading failures and improves reliability
tags: errors, retry, backoff, http-codes
---

## Error Handling Strategies

Handle HTTP errors and implement retry logic.

**HTTP Return Codes:**

| Code | Description         | Action                         |
| ---- | ------------------- | ------------------------------ |
| 4XX  | Malformed request   | Fix request parameters         |
| 403  | WAF limit violated  | Check request rate             |
| 429  | Rate limit exceeded | Back off, respect Retry-After  |
| 5XX  | Server error        | Retry with exponential backoff |

**Incorrect:**

```javascript
// Not handling errors at all
const response = await axios.post(url);

// Assuming 5XX means failure
if (response.status >= 500) {
  console.log("Order failed"); // Wrong! Order may have succeeded!
}
```

**Correct:**

```javascript
async function safeRequest(method, endpoint, params, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await signedRequest(method, endpoint, params);
    } catch (error) {
      const status = error.response?.status;
      const code = error.response?.data?.code;

      // Rate limit - respect Retry-After header
      if (status === 429) {
        const retryAfter = error.response.headers["retry-after"] || 60;
        console.log(`Rate limited. Retry after ${retryAfter}s`);
        await sleep(retryAfter * 1000);
        continue;
      }

      // Server error - retry with backoff (order status UNKNOWN!)
      if (status >= 500) {
        console.log("Server error, retrying...");
        await sleep(Math.pow(2, attempt) * 1000);
        continue;
      }

      // Client error - don't retry, fix the issue
      if (status >= 400 && status < 500) {
        console.error(`Client error ${code}: ${error.response?.data?.msg}`);
        throw error;
      }

      throw error;
    }
  }
  throw new Error("Max retries exceeded");
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
```

**Important:** For 5XX errors on order placement, the order status is UNKNOWN. Query order status before retrying to avoid duplicates.

Reference: [reference/general_info.md#http-return-codes](../reference/general_info.md)
