---
title: WebSocket Limits
impact: LOW
impactDescription: prevents connection drops and bans
tags: websocket, limits, connections, subscriptions
---

## WebSocket Limits

WebSocket connection and subscription limits.

**Limits:**

- Connection rate: 100 connections/second
- Max subscriptions per connection: 30
- Max connection duration: 24 hours
- Disconnect after 30s without valid subscription
- Disconnect after 60s without data flow (send PING)
- IPs repeatedly disconnected may be banned

**Correct:**

```javascript
const WebSocket = require("ws");

class MexcWebSocket {
  constructor() {
    this.subscriptions = new Set();
    this.maxSubscriptions = 30;
    this.ws = null;
    this.pingInterval = null;
  }

  connect() {
    this.ws = new WebSocket("wss://wbs-api.mexc.com/ws");

    this.ws.on("open", () => {
      console.log("Connected");
      // Start ping interval to keep connection alive
      this.pingInterval = setInterval(() => {
        this.ws.send(JSON.stringify({ method: "PING" }));
      }, 30000);
    });

    this.ws.on("close", () => {
      console.log("Disconnected");
      clearInterval(this.pingInterval);
      // Reconnect after delay
      setTimeout(() => this.reconnect(), 5000);
    });

    this.ws.on("error", (err) => {
      console.error("WebSocket error:", err);
    });
  }

  subscribe(channel) {
    if (this.subscriptions.size >= this.maxSubscriptions) {
      console.error("Max subscriptions reached (30)");
      return false;
    }

    this.ws.send(
      JSON.stringify({
        method: "SUBSCRIPTION",
        params: [channel],
      }),
    );

    this.subscriptions.add(channel);
    return true;
  }

  unsubscribe(channel) {
    this.ws.send(
      JSON.stringify({
        method: "UNSUBSCRIPTION",
        params: [channel],
      }),
    );
    this.subscriptions.delete(channel);
  }

  reconnect() {
    console.log("Reconnecting...");
    this.connect();

    // Resubscribe after connection
    this.ws.on("open", () => {
      this.subscriptions.forEach((channel) => {
        this.ws.send(
          JSON.stringify({
            method: "SUBSCRIPTION",
            params: [channel],
          }),
        );
      });
    });
  }

  // Handle 24-hour limit - reconnect before timeout
  scheduleReconnect() {
    setTimeout(
      () => {
        console.log("24-hour limit approaching, reconnecting...");
        this.ws.close();
      },
      23 * 60 * 60 * 1000,
    ); // Reconnect after 23 hours
  }
}
```

Reference: [reference/general_info.md#websocket-limits](../reference/general_info.md)
