---
title: User Data Streams Account Updates
impact: MEDIUM
impactDescription: enables real-time balance monitoring
tags: user-data, account, balance, listen-key
---

## User Data Streams Account Updates

Real-time balance and position updates.

**Listen Key Management:**

- Valid for 60 minutes after creation
- PUT request extends validity by 60 minutes
- DELETE closes the stream
- Max 60 listen keys per UID
- Max 5 WebSocket connections per listen key

**Correct:**

```javascript
const axios = require("axios");
const WebSocket = require("ws");

const apiKey = process.env.MEXC_API_KEY;
const baseURL = "https://api.mexc.com";

// 1. Create listen key (valid for 60 minutes)
const {
  data: { listenKey },
} = await axios.post(`${baseURL}/api/v3/userDataStream`, null, {
  headers: { "X-MEXC-APIKEY": apiKey },
});

// 2. Connect with listen key
const ws = new WebSocket(`wss://wbs-api.mexc.com/ws?listenKey=${listenKey}`);

// 3. Subscribe to account updates
ws.on("open", () => {
  ws.send(
    JSON.stringify({
      method: "SUBSCRIPTION",
      params: ["spot@private.account.v3.api.pb"],
    }),
  );
});

// 4. Handle account updates
ws.on("message", (data) => {
  const event = JSON.parse(data);
  if (event.channel === "spot@private.account.v3.api.pb") {
    const account = event.privateAccount;
    console.log("Asset:", account.vcoinName);
    console.log("Balance:", account.balanceAmount);
    console.log("Balance Change:", account.balanceAmountChange);
    console.log("Frozen:", account.frozenAmount);
    console.log("Frozen Change:", account.frozenAmountChange);
    console.log("Type:", account.type); // e.g., "CONTRACT_TRANSFER", "TRADE"
    console.log("Time:", account.time);
  }
});

// 5. Keep alive every 30 minutes (recommended)
setInterval(
  () => {
    axios.put(`${baseURL}/api/v3/userDataStream?listenKey=${listenKey}`, null, {
      headers: { "X-MEXC-APIKEY": apiKey },
    });
  },
  30 * 60 * 1000,
);

// 6. Close stream when done
process.on("SIGINT", async () => {
  await axios.delete(
    `${baseURL}/api/v3/userDataStream?listenKey=${listenKey}`,
    {
      headers: { "X-MEXC-APIKEY": apiKey },
    },
  );
  ws.close();
});
```

Reference: [reference/websocket_user_data_streams.md](../reference/websocket_user_data_streams.md)
