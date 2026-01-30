# Rebate Endpoints

Source: https://www.mexc.com/api-docs/spot-v3/rebate-endpoints

On this page

# Rebate Endpoints

## Get Rebate History Records

> request

```
get /api/v3/rebate/taxQuery?timestamp={{timestamp}}&signature={{signature}}
```

> response

```
{    "page": 1,      "totalRecords": 1,      "totalPageNum": 1,      "data": [        {            "spot": "0.00082273",              "futures":"0.00022487",                   "total": "0.00012126",              "uid": "221827",              "account": "154****291@qq.com",              "inviteTime": 1637651320000        },        ...        {            "spot": "0.00082273",              "futures":"0.00022487",                "total": "0.00012126",              "uid": "82937",              "account": "338****291@qq.com",              "inviteTime": 1637651320000        }    ]}
```

**Http Request**

*   **GET** `/api/v3/rebate/taxQuery`

**Permission:** SPOT\_ACCOUNT\_READ

**Weight(IP):** 1

**Request**

Name

Type

Mandatory

Description

startTime

long

NO

endTime

long

NO

page

int

NO

default 1

recvWindow

long

NO

timestamp

long

YES

signature

string

YES

**Response**

Name

Type

Description

spot

string

spot rebate,unit:usdt

futures

string

futures rebate,unit:usdt

total

string

total rebate,unit:usdt

uid

string

Invitee uid

account

string

Invitee account

inviteTime

long

invite time

If startTime and endTime are not sent, the recent 1 year's data will be returned.

## Get Rebate Records Detail

> request

```
get /api/v3/rebate/detail?timestamp={{timestamp}}&signature={{signature}}
```

> response

```
{     "page": 1,      "totalRecords": 1,      "totalPageNum": 1,      "data": [         {             "asset": "USDT",              "type": "spot",                    "rate": "0.3",              "amount": "0.0001126",              "uid": "2293729101827",              "account": "154****291@qq.com",              "tradeTime": 1637651320000,             "updateTime": 1637651320000         },         ...         {             "asset": "ETH",              "type": "spot",              "rate": "0.3",              "amount": "0.00000056",             "uid": "22937291018263",              "account": "154****291@qq.com",              "tradeTime": 1637651320000,             "updateTime": 1637928379000         }     ]}​
```

**Http Request**

*   **GET** `/api/v3/rebate/detail`

**Permission:** SPOT\_ACCOUNT\_READ

**Weight(IP):** 1

**Request**

Name

Type

Mandatory

Description

startTime

long

NO

endTime

long

NO

page

int

NO

default 1

recvWindow

long

NO

timestamp

long

YES

signature

string

YES

**Response**

Name

Type

Description

asset

string

rebate asset

type

string

rebate type: spot futures

rate

string

rebate rate

amount

string

rebate amount

uid

string

Invitee uid

account

string

Invitee account

tradeTime

long

trade time

updateTime

long

update time

If startTime and endTime are not sent, the recent 1 year's data will be returned.

## Get Self Rebate Records Detail

> request

```
get /api/v3/rebate/detail/kickback?timestamp={{timestamp}}&signature={{signature}}
```

> response

```
{    "page": 1,      "totalRecords": 27,      "totalPageNum": 3,      "data": [        {            "asset": "USDT",              "type": "spot",                    "rate": "0.3",             "amount": "0.0001126",              "uid": "2293729101827",              "account": "154****291@qq.com",              "tradeTime": 1637651320000,            "updateTime": 1637651320000        },        ...        {            "asset": "ETH",             "type": "spot",             "rate": "0.3",             "amount": "0.00000056",            "uid": "22937291018263",              "account": "154****291@qq.com",              "tradeTime": 1637651320000,            "updateTime": 1637928379000        }    ]}
```

**Http Request**

*   **GET** `/api/v3/rebate/detail/kickback`

**Permission:** SPOT\_ACCOUNT\_READ

**Weight(IP):** 1

**Request**

Name

Type

Mandatory

Description

startTime

long

NO

endTime

long

NO

page

int

NO

default 1

recvWindow

long

NO

timestamp

long

YES

signature

string

YES

**Response**

Name

Type

Description

asset

string

rebate asset

type

string

rebate type: spot futures

rate

string

rebate rate

amount

string

rebate amount

uid

string

Invitee uid

account

string

Invitee account

tradeTime

long

trade time

updateTime

long

update time

If startTime and endTime are not sent, the recent 1 year's data will be returned.

## Query ReferCode

> request

```
get /api/v3/rebate/referCode?timestamp={{timestamp}}&signature={{signature}}
```

> response

```
{    "referCode": "in3jd"}
```

**HTTP Request**

*   **GET** `/api/v3/rebate/referCode`

**Permission:** SPOT\_ACCOUNT\_READ

**Weight(IP):** 1

**Request**

Name

Type

Mandatory

Description

recvWindow

long

NO

timestamp

long

YES

signature

string

YES

**Response**

Name

Type

Description

referCode

string

referCode

## Get Affiliate Commission Record (affiliate only)

> request

```
get /api/v3/rebate/affiliate/commission?timestamp={{timestamp}}&signature={{signature}}
```

> response

```
{    "success": true,    "code": 0,    "message": null,    "data": {        "pageSize": 10,        "totalCount": 2,        "totalPage": 1,        "currentPage": 1,        "usdtAmount": null,        "totalCommissionUsdtAmount": null,        "totalTradeUsdtAmount": null,        "finished": null,        "resultList": [            {                "uid": "27121050",                "account": "",                "inviteCode": "mexc-12345",                "inviteTime": 1637145911,                "spot": "0.00000000",                "etf": "0.21131086",                "futures": "0.74546367",                "total": "0.95677453",                "deposit": null,                "firstDepositTime": null            },            {                "uid": "52813530",                "account": "",                "inviteCode": "mexc-12345",                "inviteTime": 1637145478,                "spot": "1.25023599",                "etf": "0.00000000",                "futures": "0.00000000",                "total": "1.25023599",                "deposit": "26000.00000000",                "firstDepositTime": "2021-11-19"            }        ]    }}​
```

**HTTP Request**

*   **GET** `/api/v3/rebate/affiliate/commission`

**Permission:** SPOT\_ACCOUNT\_READ

**Weight(IP):** 1

**Request**

Name

Type

Mandatory

Description

startTime

long

Yes

startTime

endTime

long

Yes

endTime

inviteCode

string

No

invite Code

page

int

No

page

pageSize

int

No

pageSize，default:10

timestamp

long

Yes

timestamp

signature

string

Yes

signature

**Response**

Name

Type

Description

uid

string

user uid

account

string

account

inviteCode

string

inviteCode

inviteTime

long

inviteTime

spot

string

spot commission(usdt)

etf

string

ETF commission(usdt)

futures

string

futures commission(usdt)

total

string

total commission(usdt)

deposit

string

deposit amount(usdt)

firstDepositTime

string

first Deposit Time

If startTime and endTime are not sent, default return the data of the last six months .

## Get Affiliate Withdraw Record (affiliate only)

> request

```
get /api/v3/rebate/affiliate/withdraw?timestamp={{timestamp}}&signature={{signature}}
```

> response

```
{    "success": true,    "code": 0,    "message": null,    "data": {        "pageSize": 10,        "totalCount": 15,        "totalPage": 2,        "currentPage": 1,        "resultList": [            {                "withdrawTime": 1682321417000,                "asset": "USDT",                "amount": "0.00001000"            },            {                "withdrawTime": 1682321405000,                "asset": "USDC",                "amount": "0.00001000"            }        ]    }}​
```

**HTTP Request**

*   **GET** `/api/v3/rebate/affiliate/withdraw`

**Permission:** SPOT\_ACCOUNT\_READ

**Weight(IP):** 1

**Request**

Name

Type

Mandatory

Description

startTime

long

No

startTime

endTime

long

No

endTime

page

int

No

page

pageSize

int

No

pageSize,default: 10

timestamp

long

Yes

timestamp

signature

string

Yes

signature

**Response**

Name

Type

Description

withdrawTime

long

withdrawTime

asset

string

withdraw asset

amount

string

withdraw amount

If startTime and endTime are not sent, the data of the last six months is returned.

## Get Affiliate Commission Detail Record (affiliate only)

> request

```
get /api/v3/rebate/affiliate/commission/detail?timestamp={{timestamp}}&signature={{signature}}
```

> response

```
{    "success": true,    "code": 0,    "message": null,    "data": {        "pageSize": 10,        "totalCount": 5,        "totalPage": 1,        "currentPage": 1,        "totalCommissionUsdtAmount": "0.0011",        "totalTradeUsdtAmount": "281.8096",        "resultList": [            {                "type": 2,                "sourceType": 2,                "state": 2,                "date": 1689264000000,                "uid": "17875073",                "rate": 0.1,                "symbol": "USDT",                "takerAmount": "170.49326",                "makerAmount": "0",                "amountCurrency": "USDT",                "usdtAmount": "170.49326",                "commission": "0.00085246",                "currency": "USDT"            }        ]    }}​
```

**HTTP Request**

*   **GET** `/api/v3/rebate/affiliate/commission/detail`

**Permission:** SPOT\_ACCOUNT\_READ

**Weight(IP):** 1

**Request**

Name

Type

Mandatory

Description

startTime

long

No

startTime

endTime

long

No

endTime

inviteCode

string

No

inviteCode

page

int

No

page

pageSize

int

No

pageSize,default: 10

type

int

No

commission type,1:spot,2:futures,3:ETF

timestamp

long

Yes

timestamp

signature

string

Yes

signature

**Response**

Name

Type

Description

totalCommissionUsdtAmount

string

total commission in usdt

totalTradeUsdtAmount

string

total trade volume in usdt

type

int

commission type,1:spot 2:futures 3:ETF

sourceType

int

sourceType,1:referral 2:sub-affiliate

state

int

commission state

date

long

trade date

uid

string

uid

rate

string

commission rate

symbol

string

symbol

takerAmount

string

taker amount

makerAmount

string

maker amount

amountCurrency

string

amount currency

usdtAmount

string

usdt amount

commission

string

commission amount

currency

string

commission currency

If startTime and endTime are not sent, the data from T-7 to T is returned. If type is not sent, the data of all types is returned,maximum 30 days data can be queried at one time.

## Get Affiliate Campaign Data (affiliate only)

> request

```
get /api/v3/rebate/affiliate/campaign?timestamp={{timestamp}}&signature={{signature}}
```

> response

```
{    "success": true,    "code": 0,    "message": null,    "data": {        "pageSize": 10,        "totalCount": 15,        "totalPage": 2,        "currentPage": 1,        "resultList": [            {                "campaign": "11kd",                "inviteCode": "mexc-11Kd",                "clickTime": 0,                "createTime": 1695125287000,                "signup": 0,                "traded": 0,                "deposited": 0,                "depositAmount": "0",                "tradingAmount": "0",                "commission": "0"            },            {                "campaign": "New10",                "inviteCode": "mexc-newcode",                "clickTime": 7,                "createTime": 1693152531000,                "signup": 0,                "traded": 0,                "deposited": 0,                "depositAmount": "0",                "tradingAmount": "0",                "commission": "0"            }        ]    }}​
```

**HTTP Request**

*   **GET** `/api/v3/rebate/affiliate/campaign`

**Permission:** SPOT\_ACCOUNT\_READ

**Weight(IP):** 1

**Request**

Name

Type

Mandatory

Description

startTime

long

No

startTime

endTime

long

No

endTime

page

int

No

page

pageSize

int

No

pageSize,default: 10

timestamp

long

Yes

timestamp

signature

string

Yes

signature

**Response**

Name

Type

Description

campaign

string

campaign name

inviteCode

string

campaign inviteCode

createTime

long

campaign createTime

clickTime

int

inviteCode clickTime

signup

int

signup number

deposited

int

deposited number

depositAmount

string

depositAmount(usdt)

tradingAmount

string

tradingAmount(usdt)

traded

int

traded number

commission

string

commission

If startTime and endTime are not sent, the data from T-7 to T is returned.

## Get Affiliate Referral Data（affiliate only）

> request

```
get /api/v3/rebate/affiliate/referral?timestamp={{timestamp}}&signature={{signature}}
```

> response

```
{    "success": true,    "code": 0,    "message": null,    "data": {        "pageSize": 10,        "totalCount": 15,        "totalPage": 2,        "currentPage": 1,        "resultList": [            {                "uid": "42469975",                "nickName": null,                "email": "",                "registerTime": 1640275818000,                "inviteCode": "mexc-12201950",                "depositAmount": "0.00000000",                "tradingAmount": "0.00000000",                "commission": "0.00000000",                "firstDepositTime": null,                "firstTradeTime": null,                "lastDepositTime": null,                "lastTradeTime": null,                "withdrawAmount": "0.00000000",                "asset": "0 USDT",                "identification": 1          }        ]    }}​
```

**HTTP Request**

*   **GET** `/api/v3/rebate/affiliate/referral`

**Permission:** SPOT\_ACCOUNT\_READ

**Weight(IP):** 1

**Request**

Name

Type

Mandatory

Description

startTime

long

No

startTime

endTime

long

No

endTime

uid

string

No

uid

inviteCode

string

No

invite code

page

int

No

page

pageSize

int

No

pageSize,default: 10

timestamp

long

Yes

timestamp

signature

string

Yes

signature

**Response**

Name

Type

Description

uid

int

uid

account

string

account email

inviteCode

string

invite code

inviteTime

long

invite time

nickName

string

nickName

firstDeposit

long

first deposit date

firstTrade

long

first trade date

lastDeposit

long

last deposit date

lastTrade

long

last trade date

depositAmount

string

deposit amount(USDT)

tradingAmount

string

trading amount(USDT)

amount

string

commission amount(USDT)

asset

string

0 USDT、1-1,000 USDT、1,000 - 10,000 USDT、 10,000 - 50,000 USDT、50,000 - 100,000 USDT、 100,000 - 500,000 USDT、500,000 - 1,000,000 USDT、 1,000,000 - 5,000,000 USDT、>5,000,000 USDT

withdrawalAmount

string

withdrawal amount(USDT)

identification

int

identification,1: Uncertified, 2: primary, 3: Advanced, 4: Institutional

If startTime and endTime are not sent, the data from T-7 to T is returned.

## Get Subaffiliates Data (affiliate only)

> request

```
get /api/v3/rebate/affiliate/subaffiliates?timestamp={{timestamp}}&signature={{signature}}
```

> response

```
{    "success": true,    "code": 0,    "message": null,    "data": {        "pageSize": 10,        "totalCount": 15,        "totalPage": 2,        "currentPage": 1,        "resultList": [            {                "subaffiliateName": "ada176@mailtemp.top ada176",                "subaffiliateMail": "ad*****6@mailtemp.top",                "campaign": "new1",                "inviteCode": "mexc-12181621",                "activationTime": 1639834136000,                "registered": 0,                "deposited": 0,                "depositAmount": "0",                "commission": "0"            },            {                "subaffiliateName": "ada165@mailtemp.top ada165",                "subaffiliateMail": "ad*****5@mailtemp.top",                "campaign": null,                "inviteCode": "1KMyk",                "activationTime": 1639831541000,                "registered": 0,                "deposited": 1,                "depositAmount": "21.15318",                "commission": "0.5161221"            }        ]    }}​
```

**HTTP Request**

*   **GET** `/api/v3/rebate/affiliate/subaffiliates`

**Permission:** SPOT\_ACCOUNT\_READ

**Weight(IP):** 1

**Request**

Name

Type

Mandatory

Description

startTime

long

No

startTime

endTime

long

No

endTime

inviteCode

string

No

inviteCode

page

int

No

page

pageSize

int

No

pageSize,default: 10

timestamp

long

Yes

timestamp

signature

string

Yes

signature

**Response**

Name

Type

Description

subaffiliateName

string

subaffiliate name

subaffiliateMail

string

subaffiliate mail

campaign

string

campaign

inviteCode

string

inviteCode

activationTime

long

activation time

registered

int

registered number

deposited

int

deposited number

depositAmount

string

deposit amount

commission

string

commission

If startTime and endTime are not sent, the data from T-7 to T is returned.