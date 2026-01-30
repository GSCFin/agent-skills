---
title: Rate Limiting
impact: LOW
impactDescription: prevents API bans and ensures reliable access
tags: rate-limits, throttling, ip-limit, uid-limit
---

## Rate Limiting

Respect IP and UID rate limits to avoid bans.

**Limits:**

- IP limit: 500 requests per 10 seconds per endpoint
- UID limit: 500 requests per 10 seconds per endpoint
- Each endpoint has independent limits
- IP and UID limits are counted separately

**Consequences:**

- 429 response = rate limited, back off
- Repeatedly violating limits = IP ban (2 minutes to 3 days)
- Retry-After header indicates wait time

**Correct:**

```javascript
class RateLimiter {
  constructor(limit = 500, windowMs = 10000) {
    this.limit = limit;
    this.windowMs = windowMs;
    this.requests = [];
  }

  async throttle() {
    const now = Date.now();
    this.requests = this.requests.filter((t) => now - t < this.windowMs);

    if (this.requests.length >= this.limit) {
      const waitTime = this.windowMs - (now - this.requests[0]);
      console.log(`Rate limit approaching, waiting ${waitTime}ms`);
      await this.sleep(waitTime);
    }

    this.requests.push(Date.now());
  }

  sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// Use one limiter per endpoint
const orderLimiter = new RateLimiter(450, 10000); // Leave buffer
const marketLimiter = new RateLimiter(450, 10000);

async function placeOrderThrottled(params) {
  await orderLimiter.throttle();
  return signedRequest("POST", "/api/v3/order", params);
}

async function getDepthThrottled(symbol) {
  await marketLimiter.throttle();
  return axios.get(`${baseURL}/api/v3/depth?symbol=${symbol}`);
}
```

Reference: [reference/general_info.md#limits](../reference/general_info.md)
