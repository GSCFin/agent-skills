---
title: Protocol Buffers Integration
impact: MEDIUM
impactDescription: required for deserializing WebSocket data
tags: protobuf, websocket, deserialization, binary
---

## Protocol Buffers Integration

MEXC WebSocket uses Protocol Buffers format for efficient data transfer.

**1. Get Proto Files:**

```bash
git clone https://github.com/mexcdevelop/websocket-proto
```

**2. Generate Deserialization Code:**

```bash
# For Node.js
npm install protobufjs
protoc --js_out=import_style=commonjs,binary:. *.proto

# For Python
protoc *.proto --python_out=./

# Other languages supported: C++, C#, Go, Ruby, PHP
```

**3. Deserialize in JavaScript:**

```javascript
const protobuf = require("protobufjs");
const WebSocket = require("ws");

// Load proto definition
const root = await protobuf.load("./PushDataV3ApiWrapper.proto");
const PushDataWrapper = root.lookupType("PushDataV3ApiWrapper");

const ws = new WebSocket("wss://wbs-api.mexc.com/ws");

ws.on("open", () => {
  ws.send(
    JSON.stringify({
      method: "SUBSCRIPTION",
      params: ["spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT"],
    }),
  );
});

ws.on("message", (buffer) => {
  try {
    // Check if it's a JSON response (subscription confirmation, ping/pong)
    const text = buffer.toString();
    if (text.startsWith("{")) {
      const json = JSON.parse(text);
      console.log("JSON response:", json);
      return;
    }

    // Decode protobuf message
    const message = PushDataWrapper.decode(buffer);
    const data = PushDataWrapper.toObject(message);

    console.log("Channel:", data.channel);
    console.log("Symbol:", data.symbol);
    console.log("Send Time:", data.sendTime);

    // Access specific payloads based on channel
    if (data.publicDeals) {
      data.publicDeals.dealsList.forEach((deal) => {
        console.log(`Trade: ${deal.price} x ${deal.quantity}`);
      });
    }
  } catch (err) {
    console.error("Decode error:", err);
  }
});
```

**Python Example:**

```python
import PushDataV3ApiWrapper_pb2

# Deserialize
result = PushDataV3ApiWrapper_pb2.PushDataV3ApiWrapper()
result.ParseFromString(buffer)

print(f"Channel: {result.channel}")
print(f"Symbol: {result.symbol}")
```

Reference: [reference/websocket_market_streams.md#protocol-buffers-integration](../reference/websocket_market_streams.md)
