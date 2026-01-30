---
title: Base Configuration
impact: CRITICAL
impactDescription: ensures correct API connectivity and timing
tags: configuration, base-url, headers, recv-window
---

## Base Configuration

Configure base URLs, headers, and timing parameters for MEXC API.

**Incorrect:**

```javascript
// Wrong header key (Binance style)
const headers = { "X-MBX-APIKEY": apiKey };

// recvWindow too large
const params = { recvWindow: 120000 }; // Max is 60000!
```

**Correct:**

```javascript
const config = {
  rest: "https://api.mexc.com",
  ws: "wss://wbs-api.mexc.com/ws",
  headers: {
    "X-MEXC-APIKEY": process.env.MEXC_API_KEY,
    "Content-Type": "application/json",
  },
  recvWindow: 5000, // Recommended: 5000ms or less, max: 60000ms
};

// Timing security validation (server-side logic):
// if (timestamp < serverTime + 1000 && serverTime - timestamp <= recvWindow)
//   process request
// else
//   reject request
```

**Sync Time Before Requests:**

```javascript
async function getServerTimeDiff() {
  const localTime = Date.now();
  const response = await axios.get(`${config.rest}/api/v3/time`);
  const serverTime = response.data.serverTime;
  return serverTime - localTime;
}

// Use timeDiff to adjust timestamps if needed
const timeDiff = await getServerTimeDiff();
const adjustedTimestamp = Date.now() + timeDiff;
```

Reference: [reference/general_info.md#timing-security](../reference/general_info.md)
