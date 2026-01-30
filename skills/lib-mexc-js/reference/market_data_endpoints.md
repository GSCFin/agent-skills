# Market Data Endpoints

Source: https://www.mexc.com/api-docs/spot-v3/market-data-endpoints

On this page

# Market Data Endpoints

## Download Historical Market Data

Provides kline and trading data for all Spot pairs since 01-01-2023:[Historical Market Data](https://www.mexc.co/zh-CN/market-data-download "Historical Market Data")

## Test Connectivity

> Response

```
{}
```

*   **GET** `/api/v3/ping`

Test connectivity to the Rest API.

**Weight(IP):** 1

Parameter:

NONE

## Check Server Time

> Response

```
{    "serverTime" : 1645539742000}
```

*   **GET** `/api/v3/time`

**Weight(IP):** 1

Parameter:

NONE

## API default symbol

> Request

```
GET /api/v3/defaultSymbols
```

> Response

```
{    "code": 200,    "data": [        "GENE1USDT",        "SNTUSDT",        "SQUAWKUSDT",        "HEGICUSDT",        "GUMUSDT"    ],    "msg": null}
```

*   **GET** `/api/v3/defaultSymbols`

**Weight(IP):** 1

**Request**

NONE

**Response**

Name

Type

Description

symbol

string

symbol

## Query Offline Symbols

Get information on trading pairs that have been suspended or delisted.

> Request

```
GET /api/v3/symbol/offline
```

> Response

```
{    "data": [        {            "symbol": "LVNUSDT",            "state": 3        },        {            "symbol": "LOKAUSDT",            "state": 3,            "offlineTime": 1724125694000        },        {            "symbol": "PIASBTC",            "state": 3,            "offlineTime": 1669886455000        },        {            "symbol": "SUBUSDT",            "state": 3,            "offlineTime": 1738245924000        },        {            "symbol": "BARTOLD2USDT",            "state": 3,            "offlineTime": 1653753197000        },        {            "symbol": "MISHAUSDT",            "state": 3,            "offlineTime": 1740751476000        },        {            "symbol": "OPENOLDETH",            "state": 3        }    ]}
```

*   **GET** `/api/v3/symbol/offline`

**Weight(IP):** 10

**Request**

NONE

**Response**

Name

Type

Description

symbol

string

symbol

state

int

Status: 2 - Suspended, 3 - Delisted

offlineTime

long

Delisting time (ms)

## Exchange Information

> Response

```
{    "timezone": "CST",    "serverTime": 1765342336768,    "rateLimits": [],    "exchangeFilters": [],    "symbols": [        {            "symbol": "BTCUSDT",            "status": "1",            "baseAsset": "BTC",            "baseAssetPrecision": 8,            "quoteAsset": "USDT",            "quotePrecision": 2,            "quoteAssetPrecision": 2,            "baseCommissionPrecision": 8,            "quoteCommissionPrecision": 2,            "orderTypes": [                "LIMIT",                "MARKET",                "LIMIT_MAKER"            ],            "isSpotTradingAllowed": false,            "isMarginTradingAllowed": false,            "quoteAmountPrecision": "1",            "baseSizePrecision": "0.000001",            "permissions": [                "SPOT"            ],            "filters": [                {                    "filterType": "PERCENT_PRICE_BY_SIDE",                    "bidMultiplierUp": "0.005",                    "askMultiplierDown": "0.005"                }            ],            "maxQuoteAmount": "4000000",            "makerCommission": "0",            "takerCommission": "0.0005",            "quoteAmountPrecisionMarket": "1",            "maxQuoteAmountMarket": "4000000",            "fullName": "Bitcoin",            "tradeSideType": 1,            "contractAddress": "",            "conceptPlateIds": [                50,                5,                39,                12            ],            "st": false        }    ]}
```

*   **GET** `/api/v3/exchangeInfo`

Current exchange trading rules and symbol information

**Weight(IP):** 10

**Parameter**:

There are 3 possible options:

Method

**Example**

No parameter

curl -X GET "[https://api.mexc.com/api/v3/exchangeInfo](https://api.mexc.com/api/v3/exchangeInfo "https://api.mexc.com/api/v3/exchangeInfo")"

symbol

curl -X GET "[https://api.mexc.com/api/v3/exchangeInfo?symbol=MXUSDT](https://api.mexc.com/api/v3/exchangeInfo?symbol=MXUSDT "https://api.mexc.com/api/v3/exchangeInfo?symbol=MXUSDT")"

symbols

curl -X GET "[https://api.mexc.com/api/v3/exchangeInfo?symbols=MXUSDT,BTCUSDT](https://api.mexc.com/api/v3/exchangeInfo?symbols=MXUSDT,BTCUSDT "https://api.mexc.com/api/v3/exchangeInfo?symbols=MXUSDT,BTCUSDT")"

**Response:**

Name

Type

Description

timezone

string

timezone

serverTime

long

server Time

rateLimits

Array

rate Limits

exchangeFilters

Array

exchange Filters

symbol

String

symbol

status

String

status:1 - online, 2 - Pause, 3 - offline

baseAsset

String

base Asset

baseAssetPrecision

Int

base Asset Precision

quoteAsset

String

quote Asset

quotePrecision

Int

quote Precision

quoteAssetPrecision

Int

quote Asset Precision

baseCommissionPrecision

Int

base Commission Precision

quoteCommissionPrecision

Int

quote Commission Precision

orderTypes

Array

ENUM: [Order Type](/api-docs/spot-v3/public-api-definitions#order-type "Order Type")

isSpotTradingAllowed

Boolean

allow api spot trading

isMarginTradingAllowed

Boolean

allow api margin trading

permissions

Array

permissions

filterType

String

filter type:PERCENT\_PRICE\_BY\_SIDE

bidMultiplierUp

String

bidMultiplierUp

askMultiplierDown

String

askMultiplierDown

maxQuoteAmount

String

max Quote Amount

makerCommission

String

marker Commission

takerCommission

String

taker Commission

quoteAmountPrecision

string

min order amount

baseSizePrecision

string

min order quantity

quoteAmountPrecisionMarket

string

min order amount in market order

maxQuoteAmountMarket

String

max quote Amount in market order

tradeSideType

String

tradeSide Type:1 - All, 2 - buy order only, 3 - Sell order only, 4 - Close

contractAddress

String

contract Address

st

String

symbol st status:false,true

filter parameter description:

*   lastPrice means using the latest trade price, orderPrice means the order placement price.
*   For buy orders (only for LIMIT, IMMEDIATE\_OR\_CANCEL, FILL\_OR\_KILL): `orderPrice <= lastPrice * bidMultiplierUp`
*   For sell orders: `orderPrice >= lastPrice * askMultiplierDown`

## Order Book

> Response

```
{  "lastUpdateId": 1112416,  "bids": [      ["15.00000", "49999.00000"]  ],  "asks": [    ["14.0000", "1.0000"]  ]}
```

*   **GET** `/api/v3/depth`

**Weight(IP):** 1

Parameter:

Name

Type

Mandatory

Description

Scope

symbol

string

YES

Symbol

limit

integer

NO

Returen number

default 100; max 5000

Response:

Name

Type

Description

lastUpdateId

long

Last Update Id

bids

list

Bid \[Price, Quantity \]

asks

list

Ask \[Price, Quantity \]

## Recent Trades List

> Response

```
[  {    "id": null,    "price": "23",    "qty": "0.478468",    "quoteQty": "11.004764",    "time": 1640830579240,    "isBuyerMaker": true,    "isBestMatch": true  }]
```

*   **GET** `/api/v3/trades`

**Weight(IP):** 5

Parameter:

Name

Type

Mandatory

Description

Scope

symbol

string

YES

limit

integer

NO

Default 500; max 1000

Response:

Name

Description

id

Trade id

price

Price

qty

Number

quoteQty

Trade total

time

Trade time

isBuyerMaker

Was the buyer the maker?

isBestMatch

Was the trade the best price match?

## Compressed/Aggregate Trades List

> Response

```
[  {    "a": null,    "f": null,    "l": null,    "p": "46782.67",    "q": "0.0038",    "T": 1641380483000,    "m": false,    "M": true  }]
```

*   **GET** `/api/v3/aggTrades`

**Weight(IP):** 1

Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same price will have the quantity aggregated.

Parameters:

Name

Type

Mandatory

Description

Scope

symbol

string

YES

startTime

long

NO

Timestamp in ms to get aggregate trades from INCLUSIVE.

endTime

long

NO

Timestamp in ms to get aggregate trades until INCLUSIVE.

limit

integer

NO

Default 500; max 1000.

startTime and endTime must be used at the same time.

Response:

Name

Description

a

Aggregate tradeId

f

First tradeId

l

Last tradeId

p

Price

q

Quantity

T

Timestamp

m

Was the buyer the maker?

M

Was the trade the best price match?

## Kline/Candlestick Data

> Response

```
[  [    1640804880000,     "47482.36",     "47482.36",     "47416.57",     "47436.1",     "3.550717",     1640804940000,     "168387.3"  ]]
```

*   **GET** `/api/v3/klines`

**Weight(IP):** 1

Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

Parameters:

Name

Type

Mandatory

Description

symbol

string

YES

interval

ENUM

YES

ENUM: [Kline Interval](/api-docs/spot-v3/public-api-definitions#kline-interval "Kline Interval")

startTime

long

NO

endTime

long

NO

limit

integer

NO

Default 500; max 1000.

Response:

Index

Description

0

Open time

1

Open

2

High

3

Low

4

Close

5

Volume

6

Close time

7

Quote asset volume

## Current Average Price

> Response

```
{  "mins": 5,  "price": "9.35751834"}
```

*   **GET** `/api/v3/avgPrice`

**Weight(IP):** 1

Parameters:

Name

Type

Mandatory

Description

symbol

string

YES

Response:

Name

Description

mins

Average price time frame

price

Price

## 24hr Ticker Price Change Statistics

> Response

```
{    "symbol": "BTCUSDT",    "priceChange": "184.34",    "priceChangePercent": "0.00400048",    "prevClosePrice": "46079.37",    "lastPrice": "46263.71",    "bidPrice": "46260.38",    "bidQty": "",    "askPrice": "46260.41",    "askQty": "",    "openPrice": "46079.37",    "highPrice": "47550.01",    "lowPrice": "45555.5",    "volume": "1732.461487",    "quoteVolume": null,    "openTime": 1641349500000,    "closeTime": 1641349582808,    "count": null}or[  {    "symbol": "BTCUSDT",    "priceChange": "184.34",    "priceChangePercent": "0.00400048",    "prevClosePrice": "46079.37",    "lastPrice": "46263.71",    "bidPrice": "46260.38",    "bidQty": "",    "askPrice": "46260.41",    "askQty": "",    "openPrice": "46079.37",    "highPrice": "47550.01",    "lowPrice": "45555.5",    "volume": "1732.461487",    "quoteVolume": null,    "openTime": 1641349500000,    "closeTime": 1641349582808,    "count": null  },  {    "symbol": "ETHUSDT",    "priceChange": "184.34",    "priceChangePercent": "0.00400048",    "prevClosePrice": "46079.37",    "lastPrice": "46263.71",    "bidPrice": "46260.38",    "bidQty": "",    "askPrice": "46260.41",    "askQty": "",    "openPrice": "46079.37",    "highPrice": "47550.01",    "lowPrice": "45555.5",    "volume": "1732.461487",    "quoteVolume": null,    "openTime": 1641349500000,    "closeTime": 1641349582808,    "count": null  }]
```

*   **GET** `/api/v3/ticker/24hr`

**Weight(IP):**

Parameter

Symbols Provided

Weight

symbol

1

1

symbols

all

40

Parameters:

Name

Type

Mandatory

Description

symbol

string

NO

If the symbol is not sent, tickers for all symbols will be returned in an array.

Response:

Name

Description

symbol

Symbol

priceChange

price Change

priceChangePercent

price change percent

prevClosePrice

Previous close price

lastPrice

Last price

lastQty

Last quantity

bidPrice

Bid best price

bidQty

Bid best quantity

askPrice

Ask best price

askQty

Ask best quantity

openPrice

Open

highPrice

High

lowPrice

Low

volume

Deal volume

quoteVolume

Quote asset volume

openTime

Start time

closeTime

Close time

count

## Symbol Price Ticker

> Response

```
{    "symbol": "BTCUSDT",    "price": "184.34"}or[  {    "symbol": "BTCUSDT",    "price": "6.65"  },  {    "symbol": "ETHUSDT",    "price": "5.65"  }]
```

*   **GET** `/api/v3/ticker/price`

**Weight(IP):**

Parameter

Symbols Provided

Weight

symbol

1

1

symbols

all

2

Parameters:

Name

Type

Mandatory

Description

symbol

string

NO

If the symbol is not sent, all symbols will be returned in an array.

Response:

Name

Description

symbol

price

Last price

## Symbol Order Book Ticker

> Response

```
{  "symbol": "AEUSDT",  "bidPrice": "0.11001",  "bidQty": "115.59",  "askPrice": "0.11127",  "askQty": "215.48"}OR[  {    "symbol": "AEUSDT",    "bidPrice": "0.11001",    "bidQty": "115.59",    "askPrice": "0.11127",    "askQty": "215.48"  },  {    "symbol": "AEUSDT",    "bidPrice": "0.11001",    "bidQty": "115.59",    "askPrice": "0.11127",    "askQty": "215.48"  }]
```

*   **GET** `/api/v3/ticker/bookTicker`

**Weight(IP):** 1

Best price/qty on the order book for a symbol or symbols.

Parameters:

Name

Type

Mandatory

Description

symbol

string

NO

If the symbol is not sent, all symbols will be returned in an array.

Response:

Name

Description

symbol

Symbol

bidPrice

Best bid price

bidQty

Best bid quantity

askPrice

Best ask price

askQty

Best ask quantity