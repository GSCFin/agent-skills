---
title: Authentication & Signatures
impact: CRITICAL
impactDescription: prevents API access failures and security issues
tags: authentication, signature, hmac, sha256, api-key
---

## Authentication & Signatures

MEXC API endpoints require authentication using an API Key and HMAC-SHA256 signature. The signature must be lowercase hex.

**Incorrect (common mistakes):**

```javascript
// Sending secret key over the wire
const params = { symbol: "BTCUSDT", secret: "MY_SECRET_KEY" };

// Using wrong timestamp unit (seconds instead of milliseconds)
const timestamp = Math.floor(Date.now() / 1000); // Wrong!

// Uppercase signature (will fail verification)
const signature = crypto
  .createHmac("sha256", secret)
  .update(query)
  .digest("hex")
  .toUpperCase();
```

**Correct:**

```javascript
const crypto = require("crypto");
const axios = require("axios");

const apiKey = "YOUR_API_KEY";
const apiSecret = "YOUR_SECRET_KEY";
const baseURL = "https://api.mexc.com";

async function signedRequest(method, endpoint, params = {}) {
  const timestamp = Date.now(); // Milliseconds!
  const queryString = new URLSearchParams({ ...params, timestamp }).toString();

  // Signature must be lowercase hex
  const signature = crypto
    .createHmac("sha256", apiSecret)
    .update(queryString)
    .digest("hex");

  const url = `${baseURL}${endpoint}?${queryString}&signature=${signature}`;

  return axios({
    method,
    url,
    headers: {
      "X-MEXC-APIKEY": apiKey, // Note: X-MEXC-APIKEY, not X-MBX-APIKEY
      "Content-Type": "application/json",
    },
  });
}
```

**Note:** When mixing query string and body parameters, concatenate WITHOUT `&` separator between them.

Reference: [reference/general_info.md#signed](../reference/general_info.md)
