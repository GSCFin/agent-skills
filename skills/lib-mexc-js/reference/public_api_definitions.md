# Public API Definitions

Source: https://www.mexc.com/api-docs/spot-v3/public-api-definitions

On this page

# Public API Definitions

## ENUM definitions

### Order side

*   BUY
*   SELL

### Order type

*   LIMIT
*   MARKET
*   LIMIT\_MAKER
*   IMMEDIATE\_OR\_CANCEL
*   FILL\_OR\_KILL
*   STOP\_MARKET\_ORDER (Query only)

### Order Status

*   NEW Uncompleted
*   FILLED Filled
*   PARTIALLY\_FILLED Partially filled
*   CANCELED Canceled
*   PARTIALLY\_CANCELED Partially canceled

### Deposit Status

*   1 SMALL
*   2 TIME\_DELAY
*   3 LARGE\_DELAY
*   4 PENDING
*   5 SUCCESS
*   6 AUDITING
*   7 REJECTED
*   8 REFUND
*   9 PRE\_SUCCESS
*   10 INVALID
*   11 RESTRICTED
*   12 COMPLETED

### Withdraw Status

*   1 APPLY
*   2 AUDITING
*   3 WAIT
*   4 PROCESSING
*   5 WAIT\_PACKAGING
*   6 WAIT\_CONFIRM
*   7 SUCCESS
*   8 FAILED
*   9 CANCEL
*   10 MANUAL

### Kline Interval

*   1m 1 minute
*   5m 5 minute
*   15m 15 minute
*   30m 30 minute
*   60m 60 minute
*   4h 4 hour
*   1d 1 day
*   1W 1 week
*   1M 1 month

### changed type

*   WITHDRAW withdraw
*   WITHDRAW\_FEE withdraw fee
*   DEPOSIT deposit
*   DEPOSIT\_FEE deposit fee
*   ENTRUST deal
*   ENTRUST\_PLACE place order
*   ENTRUST\_CANCEL cancel order
*   TRADE\_FEE trade fee
*   ENTRUST\_UNFROZEN return frozen order funds
*   SUGAR airdrop
*   ETF\_INDEX ETF place order