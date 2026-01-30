---
name: lib-mexc-js
description: Comprehensive guide for MEXC Spot V3 API (REST & WebSocket with Protocol Buffers) including trading, market data, and user data streams. Triggers on tasks involving MEXC API integration, crypto trading bots, market data streams, or wallet operations.
license: MIT
metadata:
  author: mexc-dev-community
  version: "1.0.0"
---

# MEXC Spot API Skill

Comprehensive guide for integrating with the MEXC Spot V3 API, formatted for AI agents. Covers REST API, WebSocket Streams (with Protocol Buffers), and User Data Streams.

## When to Apply

Reference these guidelines when:

- Integrating MEXC Spot API for trading or market data
- Implementing WebSocket connections with Protocol Buffers
- Handling HMAC-SHA256 authentication signatures
- Setting up User Data Streams for account/order updates
- Debugging error codes or handling rate limits
- Managing wallet operations (deposit/withdraw)
- Working with sub-accounts

## Rule Categories by Priority

| Priority | Category          | Impact   | Prefix          |
| -------- | ----------------- | -------- | --------------- |
| 1        | Authentication    | CRITICAL | `setup-`        |
| 2        | REST API Trading  | HIGH     | `rest-trading-` |
| 3        | REST API Data     | HIGH     | `rest-`         |
| 4        | WebSocket Streams | MEDIUM   | `ws-streams-`   |
| 5        | User Data Streams | MEDIUM   | `uds-`          |
| 6        | Error Handling    | MEDIUM   | `errors-`       |
| 7        | Rate Limiting     | LOW      | `limits-`       |
| 8        | Wallet Operations | LOW      | `wallet-`       |
| 9        | Sub-Accounts      | LOW      | `subaccount-`   |

## Quick Reference

### 1. Authentication (CRITICAL)

- `setup-authentication` - Generate HMAC-SHA256 signatures correctly
- `setup-base-config` - Configure base URLs and headers

### 2. REST API Trading (HIGH)

- `rest-trading-orders` - Place, query, and cancel orders via REST
- `rest-trading-batch` - Batch order operations (up to 20 orders)

### 3. REST API Data (HIGH)

- `rest-market-data` - Get order book, trades, klines, and tickers
- `rest-account-info` - Fetch account balances and trade history

### 4. WebSocket Streams (MEDIUM)

- `ws-streams-market` - Subscribe to real-time market data streams
- `ws-streams-orderbook` - Manage local order book with depth streams
- `ws-streams-protobuf` - Integrate Protocol Buffers for deserialization

### 5. User Data Streams (MEDIUM)

- `uds-account-updates` - Handle balance and account position updates
- `uds-order-updates` - Process order status and trade notifications

### 6. Error Handling (MEDIUM)

- `errors-handling` - Interpret error codes and implement retries
- `errors-codes` - Complete error code reference

### 7. Rate Limiting (LOW)

- `limits-rate-limiting` - Respect IP and UID rate limits
- `limits-websocket` - WebSocket connection and subscription limits

### 8. Wallet Operations (LOW)

- `wallet-withdraw` - Withdraw assets to external addresses
- `wallet-deposit` - Generate and query deposit addresses

### 9. Sub-Accounts (LOW)

- `subaccount-management` - Create and manage sub-accounts

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/setup-authentication.md
rules/rest-trading-orders.md
rules/ws-streams-protobuf.md
rules/errors-codes.md
```

## Reference Documentation

Local reference docs in `reference/` directory:

- [general_info.md](reference/general_info.md) - Base endpoint, authentication, error codes
- [spot_account_trade.md](reference/spot_account_trade.md) - Trading endpoints
- [market_data_endpoints.md](reference/market_data_endpoints.md) - Market data endpoints
- [websocket_market_streams.md](reference/websocket_market_streams.md) - WebSocket streams
- [websocket_user_data_streams.md](reference/websocket_user_data_streams.md) - User data streams

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
