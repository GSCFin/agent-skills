# Futures

Source: https://www.mexc.com/api-docs/futures/update-log

# Update log

Effective Time (UTC+8)

Endpoint

Update Type

Description

2021-01-15

\*

Added

Release of contract API

2021-03-30

\*

adjust

the following endpoints to access the paths and the data return format (the original paths still supported, but will gradually abandoned) : get the user’s all history orders, get the user’s ongoing orders, get the user’s history position information, get the stop-limit orders list, get the trigger orders list, get the user’s all transaction details

2022-07-07

\*

Added

Get the contract information endpoint add a new field: apiAllowed(true or false),means Whether support API

2022-07-25

\*

maintenance

place order endpoints and cancel orders endpoints will be closed temporarily. The query endpoints can still be used

2024-01-31

\*

adjust

ws base url update:wss://contract.mexc.com/edge

2025-04-09

\*

adjust

Subscribe to ws incremental depth data, with zipped push by default: `compress` is set to `true`

2025-08-21

\*

adjust

Subscribe to ws deal data, with zipped push by default: `compress` is set to `true`

2025-11-03

\*

Added

Comprehensive update to the Contract API, including internationalization support and error code optimization

2025-11-25

\*

Added

Contract WebSocket underwent an overall update, including web/APP login

2025-12-02

\*

Added

Added endpoint `api/v1/private/order/list/open_orders`, removed endpoints `api/v1/private/order/open_orders`, `api/v1/private/order/close_orders`

2025-12-05

\*

Added

Added WebSocket Incremental Order Book Maintenance Mechanism

2025-12-08

\*

Added

Added WebSocket channel push frequency description

2026-01-19

\*

Added

Added STP and Batch Order API; Futures API domain changed to: `https://api.mexc.com`