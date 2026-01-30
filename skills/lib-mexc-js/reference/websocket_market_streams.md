# Websocket Market Streams

Source: https://www.mexc.com/api-docs/spot-v3/websocket-market-streams

On this page

# Websocket Market Streams

*   The base endpoint is: **[wss://wbs-api.mexc.com/ws](https://wbs-api.mexc.com/ws "wss://wbs-api.mexc.com/ws")**
*   Each connection to **[wss://wbs-api.mexc.com/ws](https://wbs-api.mexc.com/ws "wss://wbs-api.mexc.com/ws")** is valid for no more than 24 hours. Please handle disconnections and reconnections properly.
*   All trading pair names in the symbol must be in **uppercase**. For example: `spot@public.aggre.deals.v3.api.pb@&lt;symbol&gt;`  
    Example: `spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT`
*   If there is no valid subscription on the websocket, the server will actively disconnect after **30 seconds**. If the subscription is successful but there is no data flow, the server will disconnect after **one minute**. The client can send a ping to keep the connection alive.
*   One ws connection supports a maximum of 30 subscriptions.
*   Please process the data according to the parameters returned in the documentation. Parameters not returned in the documentation will be optimized soon, so please do not use them.

## Live Subscription/Unsubscription to Data Streams

*   The following data can be sent via websocket to subscribe or unsubscribe from data streams. Examples are provided below.
*   The `id` in the response is an unsigned integer and serves as the unique identifier for communication.
*   If the `msg` in the response matches the corresponding request field, it indicates that the request was sent successfully.

## Protocol Buffers Integration

The current websocket push uses the protobuf format. The specific integration process is as follows:

1.**PB File Definition**  
The PB definition files can be obtained via the provided link:[](https://github.com/mexcdevelop/websocket-proto "https://github.com/mexcdevelop/websocket-proto")[https://github.com/mexcdevelop/websocket-proto](https://github.com/mexcdevelop/websocket-proto "https://github.com/mexcdevelop/websocket-proto")

2.**Generate Deserialization Code**  
Use the tool available at [](https://github.com/protocolbuffers/protobuf "https://github.com/protocolbuffers/protobuf")[https://github.com/protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf "https://github.com/protocolbuffers/protobuf") to compile the .proto files and generate deserialization code.

> **Java**

```
protoc *.proto --java_out=python custom_path
```

> **Python**

```
protoc *.proto --python_out=python custom_path
```

> **Others**

```
Multiple languages are supported, including C++, C#, Go, Ruby, PHP, JS, etc. For details, see <a href="https://github.com/protocolbuffers/protobuf" title="https://github.com/protocolbuffers/protobuf" aria-label="https://github.com/protocolbuffers/protobuf" rel="nofollow">https://github.com/protocolbuffers/protobuf</a>.
```

3.**Data Deserialization**  
Use the code generated in the previous step to deserialize the data.

> **Java**  
> Include the protobuf-java dependency:

```
<dependency>    <groupId>com.google.protobuf</groupId>    <artifactId>protobuf-java</artifactId>    <version>{protobuf.version}</version> <!-- Specify the version as per your project requirements --></dependency>
```

```
//Parsing example:// Assemble the objectPushDataV3ApiWrapper pushDataV3ApiWrapper = PushDataV3ApiWrapper.newBuilder()        .setChannel("spot@public.aggre.depth.v3.api.pb@10ms")        .setSymbol("BTCUSDT")        .setSendTime(System.currentTimeMillis())        .build();// Serialize to a byte arraybyte[] serializedData = pushDataV3ApiWrapper.toByteArray();// Deserialize into a PushDataV3ApiWrapper objectPushDataV3ApiWrapper resultV3 = PushDataV3ApiWrapper.parseFrom(serializedData);
```

> **Python**

```
#Parsing example:import PushDataV3ApiWrapper_pb2# Assemble the objectpushData = PushDataV3ApiWrapper_pb2.PushDataV3ApiWrapper()pushData.channel = 'spot@public.aggre.depth.v3.api.pb@10ms'pushData.symbol = 'BTCUSDT'# Serialize to a stringserializedData = pushData.SerializeToString()# Deserialize into a PushDataV3ApiWrapper objectresult = PushDataV3ApiWrapper_pb2.PushDataV3ApiWrapper()result.ParseFromString(serializedData)print(result)
```

* * *

### Subscribe to a Data Stream

> **Subscription Channel Response**

```
{  "id": 0,  "code": 0,  "msg": "spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT"}
```

*   **Request**

```
{ "method": "SUBSCRIPTION", "params": ["spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT"]}
```

* * *

### Unsubscribe from a Data Stream

> **Unsubscription Response**

```
{  "id": 0,  "code": 0,  "msg": "spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT"}
```

*   **Request**

```
{ "method": "UNSUBSCRIPTION", "params": ["spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT"]}
```

* * *

### PING/PONG Mechanism

> **PING/PONG Response**

```
{  "id": 0,  "code": 0,  "msg": "PONG"}
```

*   **Request**

```
{"method": "PING"}
```

* * *

## Trade Streams

> **Request:**

```
{    "method": "SUBSCRIPTION",    "params": [        "spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT"    ]}
```

> **Response:**

```
{  "channel": "spot@public.aggre.deals.v3.api.pb@100ms@BTCUSDT",  "publicdeals": {    "dealsList": [      {        "price": "93220.00", // Trade price        "quantity": "0.04438243", // Trade quantity        "tradetype": 2, // Trade type (1: Buy, 2: Sell)        "time": 1736409765051 // Trade time      }    ],    "eventtype": "spot@public.aggre.deals.v3.api.pb@100ms" // Event type   },  "symbol": "BTCUSDT", // Trading pair  "sendtime": 1736409765052 // Event time}
```

**Request Parameter:** `spot@public.aggre.deals.v3.api.pb@(100ms|10ms)@<symbol>`

The Trade Streams push raw trade information; each trade has a unique buyer and seller

**Response Parameters:**

Parameter

Data Type

Description

dealsList

array

Trade information

price

string

Trade price

quantity

string

Trade quantity

tradetype

int

Trade type (1: Buy, 2: Sell)

time

long

Trade time

eventtype

string

Event type

symbol

string

Trading pair

sendtime

long

Event time

* * *

## K-line Streams

> **Request:**

```
{    "method": "SUBSCRIPTION",    "params": [        "spot@public.kline.v3.api.pb@BTCUSDT@Min15"    ]}
```

> **Response:**

```
{  "channel": "spot@public.kline.v3.api.pb@BTCUSDT@Min15",  "publicspotkline": {    "interval": "Min15", // K-line interval    "windowstart": 1736410500, // Start time of the K-line    "openingprice": "92925", // Opening trade price during this K-line    "closingprice": "93158.47", // Closing trade price during this K-line    "highestprice": "93158.47", // Highest trade price during this K-line    "lowestprice": "92800", // Lowest trade price during this K-line    "volume": "36.83803224", // Trade volume during this K-line    "amount": "3424811.05", // Trade amount during this K-line    "windowend": 1736411400 // End time of the K-line     },  "symbol": "BTCUSDT",  "symbolid": "2fb942154ef44a4ab2ef98c8afb6a4a7",  "createtime": 1736410707571}
```

The Kline/Candlestick Stream push updates to the current klines/candlestick every second.

**Request Parameter:** `spot@public.kline.v3.api.pb@<symbol>@<interval>`

**Response Parameters:**

Parameter

Data Type

Description

publicspotkline

object

K-line information

interval

string

K-line interval

windowstart

long

Start time of the K-line

openingprice

bigDecimal

Opening trade price during this K-line

closingprice

bigDecimal

Closing trade price during this K-line

highestprice

bigDecimal

Highest trade price during this K-line

lowestprice

bigDecimal

Lowest trade price during this K-line

volume

bigDecimal

Trade volume during this K-line

amount

bigDecimal

Trade amount during this K-line

windowend

long

End time of the K-line

symbol

string

Trading pair

symbolid

string

Trading pair ID

createtime

long

Event time

**K-line Interval Parameters:**

*   Min: Minutes; Hour: Hours; Day: Days; Week: Weeks; M: Month

Available intervals:

*   Min1
*   Min5
*   Min15
*   Min30
*   Min60
*   Hour4
*   Hour8
*   Day1
*   Week1
*   Month1

* * *

## Diff.Depth Stream

> **Request:**

```
{    "method": "SUBSCRIPTION",    "params": [        "spot@public.aggre.depth.v3.api.pb@100ms@BTCUSDT"    ]}
```

> **Response:**

```
{  "channel": "spot@public.aggre.depth.v3.api.pb@100ms@BTCUSDT",  "publicincreasedepths": {    "asksList": [], // asks: Sell orders    "bidsList": [ // bids: Buy orders      {        "price": "92877.58", // Price level of change        "quantity": "0.00000000" // Quantity      }    ],    "eventtype": "spot@public.aggre.depth.v3.api.pb@100ms", // Event type    "fromVersion" : "10589632359", // from version    "toVersion" : "10589632359" // to version  },  "symbol": "BTCUSDT", // Trading pair  "sendtime": 1736411507002 // Event time}
```

If the order quantity (`quantity`) for a price level is 0, it indicates that the order at that price has been canceled or executed, and that price level should be removed.

**Request Parameter:** `spot@public.aggre.depth.v3.api.pb@(100ms|10ms)@<symbol>`

**Response Parameters:**

Parameter

Data Type

Description

price

string

Price level of change

quantity

string

Quantity

eventtype

string

Event type

version

string

Version number

symbol

string

Trading pair

sendtime

long

Event time

* * *

## Partial Book Depth Streams

This stream pushes limited level depth information. The "levels" indicate the number of order levels for buy and sell orders, which can be 5, 10, or 20 levels.

> **Request:**

```
{    "method": "SUBSCRIPTION",    "params": [        "spot@public.limit.depth.v3.api.pb@BTCUSDT@5"    ]}
```

> **Response:**

```
{  "channel": "spot@public.limit.depth.v3.api.pb@BTCUSDT@5",  "publiclimitdepths": {    "asksList": [ // asks: Sell orders      {        "price": "93180.18", // Price level of change        "quantity": "0.21976424" // Quantity      }    ],    "bidsList": [ // bids: Buy orders      {        "price": "93179.98",        "quantity": "2.82651000"      }    ],    "eventtype": "spot@public.limit.depth.v3.api.pb", // Event type    "version": "36913565463" // Version number   },  "symbol": "BTCUSDT", // Trading pair  "sendtime": 1736411838730 // Event time}
```

**Request Parameter:** `spot@public.limit.depth.v3.api.pb@<symbol>@<level>`

**Response Parameters:**

Parameter

Data Type

Description

price

string

Price level of change

quantity

string

Quantity

eventtype

string

Event type

version

string

Version number

symbol

string

Trading pair

sendtime

long

Event time

* * *

## Individual Symbol Book Ticker Streams

Pushes any update to the best bid or ask's price or quantity in real-time for a specified symbol.

> **Request:**

```
{    "method": "SUBSCRIPTION",    "params": [        "spot@public.aggre.bookTicker.v3.api.pb@100ms@BTCUSDT"    ]}
```

> **Response:**

```
{  "channel": "spot@public.aggre.bookTicker.v3.api.pb@100ms@BTCUSDT",  "publicbookticker": {    "bidprice": "93387.28",  // Best bid price    "bidquantity": "3.73485", // Best bid quantity    "askprice": "93387.29", // Best ask price    "askquantity": "7.669875" // Best ask quantity  },  "symbol": "BTCUSDT", // Trading pair  "sendtime": 1736412092433 // Event time}
```

**Request Parameter:** `spot@public.aggre.bookTicker.v3.api.pb@(100ms|10ms)@<symbol>`

**Response Parameters:**

Parameter

Data Type

Description

bidprice

string

Best bid price

bidquantity

string

Best bid quantity

askprice

string

Best ask price

askquantity

string

Best ask quantity

symbol

string

Trading pair

sendtime

long

Event time

* * *

## Individual Symbol Book Ticker Streams(Batch Aggregation)

This batch aggregation version pushes the best order information for a specified trading pair.

> **Request:**

```
{    "method": "SUBSCRIPTION",    "params": [        "spot@public.bookTicker.batch.v3.api.pb@BTCUSDT"    ]}
```

> **Response:**

```
{  "channel" : "spot@public.bookTicker.batch.v3.api.pb@BTCUSDT",  "symbol" : "BTCUSDT",  "sendTime" : "1739503249114",  "publicBookTickerBatch" : {    "items" : [ {      "bidPrice" : "96567.37",      "bidQuantity" : "3.362925",      "askPrice" : "96567.38",      "askQuantity" : "1.545255"    } ]  }}
```

**Request Parameter:** `spot@public.bookTicker.batch.v3.api.pb@<symbol>`

**Response Parameters:**

Parameter

Data Type

Description

bidprice

string

Best bid price

bidquantity

string

Best bid quantity

askprice

string

Best ask price

askquantity

string

Best ask quantity

symbol

string

Trading pair

sendtime

long

Event time

* * *

## MiniTickers

minitickers of all trading pairs in the specified timezone, pushed every 3 seconds.  
UTC value range: 24H, UTC-10, UTC-8, UTC-7, UTC-6, UTC-5, UTC-4, UTC-3, UTC+0, UTC+1, UTC+2, UTC+3, UTC+4, UTC+4:30, UTC+5, UTC+5:30, UTC+6, UTC+7, UTC+8, UTC+9, UTC+10, UTC+11, UTC+12, UTC+12:45, UTC+13

> **Request:**

```
{    "method": "SUBSCRIPTION",    "params": [        "spot@public.miniTickers.v3.api.pb@UTC+8"    ]}
```

> **Response:**

```
{    "channel": "spot@public.miniTickers.v3.api.pb@UTC+8",    "sendTime": "1755076614201",    "publicMiniTickers":    {        "items":        [            {                "symbol": "METAUSDT",                "price": "0.055",                "rate": "-0.2361",                "zonedRate": "-0.2361",                "high": "0.119",                "low": "0.053",                "volume": "814864.474",                "quantity": "10764997.16",                "lastCloseRate": "-0.2567",                "lastCloseZonedRate": "-0.2567",                "lastCloseHigh": "0.119",                "lastCloseLow": "0.053"            },            {                "symbol": "FCATUSDT",                "price": "0.0000031",                "rate": "-0.4464",                "zonedRate": "-0.4464",                "high": "0.0000066",                "low": "0.0000025",                "volume": "2825.4350195",                "quantity": "654649950.75",                "lastCloseRate": "-0.4464",                "lastCloseZonedRate": "-0.4464",                "lastCloseHigh": "0.0000066",                "lastCloseLow": "0.0000025"            },            {                "symbol": "CRVETH",                "price": "0.00022592",                "rate": "0.028",                "zonedRate": "0.028",                "high": "0.00022856",                "low": "0.00021024",                "volume": "1062.48406269",                "quantity": "4884456.998",                "lastCloseRate": "0.0276",                "lastCloseZonedRate": "0.0276",                "lastCloseHigh": "0.00022856",                "lastCloseLow": "0.00021024"            }        ]    }}
```

**Request Parameter:** `channel": "spot@public.miniTickers.v3.api.pb@<UTC-TIMEZONE>`

**Response Parameters:**

Parameter Name

Data Type

Description

symbol

string

Trading pair name

price

string

Latest price

rate

string

Price change percentage (UTC+8 timezone)

zonedRate

string

Price change percentage (local timezone)

high

string

Rolling highest price

low

string

Rolling lowest price

volume

string

Rolling turnover amount

quantity

string

Rolling trading volume

lastCloseRate

string

Previous close change percentage (UTC+8 timezone)

lastCloseZonedRate

string

Previous close change percentage (local timezone)

lastCloseHigh

string

Previous close rolling highest price

lastCloseLow

string

Previous close rolling lowest price

* * *

## MiniTicker

miniticker of the specified trading pair in the specified timezone, pushed every 3 seconds.  
UTC value range: 24H, UTC-10, UTC-8, UTC-7, UTC-6, UTC-5, UTC-4, UTC-3, UTC+0, UTC+1, UTC+2, UTC+3, UTC+4, UTC+4:30, UTC+5, UTC+5:30, UTC+6, UTC+7, UTC+8, UTC+9, UTC+10, UTC+11, UTC+12, UTC+12:45, UTC+13

> **Request:**

```
{    "method": "SUBSCRIPTION",    "params": [        "spot@public.miniTicker.v3.api.pb@MXUSDT@UTC+8"    ]}
```

> **Response:**

```
{  "channel" : "spot@public.miniTicker.v3.api.pb@MXUSDT@UTC+8",  "symbol" : "MXUSDT",  "sendTime" : "1755076752201",  "publicMiniTicker" : {    "symbol" : "MXUSDT",    "price" : "2.5174",    "rate" : "0.0766",    "zonedRate" : "0.0766",    "high" : "2.6299",    "low" : "2.302",    "volume" : "11336518.0264",    "quantity" : "4638390.17",    "lastCloseRate" : "0.0767",    "lastCloseZonedRate" : "0.0767",    "lastCloseHigh" : "2.6299",    "lastCloseLow" : "2.302"  }}
```

**Request Parameter:** `channel": "spot@public.miniTicker.v3.api.pb@<symbol>@<UTC-TIMEZONE>`

**Response Parameters:**

Parameter Name

Data Type

Description

symbol

string

Trading pair name

price

string

Latest price

rate

string

Price change percentage (UTC+8 timezone)

zonedRate

string

Price change percentage (local timezone)

high

string

Rolling highest price

low

string

Rolling lowest price

volume

string

Rolling turnover amount

quantity

string

Rolling trading volume

lastCloseRate

string

Previous close change percentage (UTC+8 timezone)

lastCloseZonedRate

string

Previous close change percentage (local timezone)

lastCloseHigh

string

Previous close rolling highest price

lastCloseLow

string

Previous close rolling lowest price

* * *

## How to Properly Maintain a Local Copy of the Order Book

1.  Connect to the WebSocket and subscribe to `spot@public.aggre.depth.v3.api.pb@(100ms|10ms)@MXBTC` to obtain incremental aggregated depth information.
2.  Access the REST API `https://api.mexc.com/api/v3/depth?symbol=MXBTC&limit=1000` to obtain a depth snapshot with 1000 levels.
3.  The `fromVersion` of each new push message should be exactly equal to the `toVersion + 1` of the previous message. Otherwise, packet loss has occurred, and reinitialization from step 2 is required.
4.  The order quantity in each push message represents the absolute value of the current order quantity at that price level, not a relative change.
5.  If the `toVersion` in the push message is smaller than the `version` in the snapshot, the message is outdated and should be ignored.
6.  If the `fromVersion` in the push message is greater than the `version` in the snapshot, data is missing between the push message and the snapshot, requiring reinitialization from step 2.
7.  Now that the `version` in the snapshot falls within the `[fromVersion, toVersion]` range of the push message, the push message can be integrated with the snapshot data as follows:
    *   If the price level in the push message already exists in the snapshot, update the quantity based on the push message.
    *   If the price level in the push message does not exist in the snapshot, insert a new entry with the quantity from the push message.
    *   If a price level in the push message has a quantity of 0, remove that price level from the snapshot.

**Note:** Since the depth snapshot has a limitation on the number of price levels, price levels outside the initial snapshot that have not changed in quantity will not appear in incremental push messages. Therefore, the local order book may differ slightly from the real order book. However, for most use cases, the 5000-depth limit is sufficient to effectively understand the market and trading activity.

* * *