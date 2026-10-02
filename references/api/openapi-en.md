# OneBullEx Open API (V2), English

> Source: https://doc.onebullex.com/#/ (onebullex-openapi-en-v2). Snapshot 2026-10-02, copied verbatim. If anything conflicts with the live docs, the live docs win.

Table of Contents
Introduction
API Overview
Authentication
Public Endpoints (V2)
Private Endpoints (V2)
WebSocket API
Error Codes
FAQ
Support
1. Introduction
1.1 Overview
OneBullEx Open API provides professional trading interface access for quantitative institutions and third-party developers. Our API supports:

Market Data: Real-time futures market data
Futures Trading: V2 version provides complete futures trading functionality
Account Management: Query positions, assets, and order history
1.2 API Version
V2 API: Futures trading endpoints
Test Environment: https://futures-openapi.1bullex.com
Production Environment: https://futures-openapi.onebullex.com
1.3 API Categories
Public Endpoints: No authentication required, used to retrieve public market data
Private Endpoints: Authentication required, used for trading operations and account queries
1.4 Request Format
Content-Type: application/json
Character Encoding: UTF-8
Time Format: Unix timestamp (milliseconds)
2. API Overview
2.1 V2 Public Endpoints (No Authentication Required)
API	Method	Description
/v2/public/time	GET	Get server time
/v2/public/symbol/list	GET	Get all trading pair configurations
/v2/public/symbol/detail	GET	Get single trading pair configuration
/v2/public/symbol/coins	GET	Get trading pair coin list
/v2/public/symbol/all	GET	Get all trading pair names
/v2/public/q/ticker	GET	Get ticker for a specific trading pair
/v2/public/q/tickers	GET	Get tickers for all trading pairs
/v2/public/q/agg-ticker	GET	Get aggregated ticker for a specific trading pair
/v2/public/q/agg-tickers	GET	Get aggregated tickers for all trading pairs
/v2/public/q/depth	GET	Get order book depth
/v2/public/q/deal	GET	Get latest trades
/v2/public/q/kline	GET	Get K-line data
/v2/public/q/mark-price	GET	Get mark price
/v2/public/q/symbol-mark-price	GET	Get mark price for a single trading pair
/v2/public/q/index-price	GET	Get index price
/v2/public/q/symbol-index-price	GET	Get index price for a single trading pair
/v2/public/q/funding-rate	GET	Get funding rate
/v2/public/q/funding-rate-record	GET	Get funding rate history
/v2/public/contract/risk-balance	GET	Get insurance fund balance records
/v2/public/contract/open-interest	GET	Get open interest for a trading pair
/v2/public/leverage/bracket/list	GET	Get leverage brackets for all trading pairs
/v2/public/leverage/bracket/detail	GET	Get leverage brackets for a single trading pair
2.2 V2 Private Endpoints (Authentication Required)
API	Method	Description
/v2/user/listen-key	GET	Get ListenKey
/v2/balance/list	GET	Get all user balances
/v2/balance/detail	GET	Get single coin balance
/v2/balance/bills	GET	Get account transaction records
/v2/balance/funding	GET	Get funding account(USDT) balance
/v2/balance/transfer	POST	Account transfer
/v2/bot/redeeming-info	GET	Get redemption queue summary
/v2/order/create	POST	Place order
/v2/order/create-batch	POST	Batch place orders
/v2/order/listUnfinished	GET	Query current open orders (single trading pair)
/v2/order/all/listUnfinished	GET	Query current open orders (multiple trading pairs)
/v2/order/list	GET	Query order list (paginated)
/v2/order/list-by-ids	POST	Query orders by ID list
/v2/order/list-history	GET	Query historical orders
/v2/order/detail	GET	Query order details by ID
/v2/order/cancel	POST	Cancel order
/v2/order/cancel-batch	POST	Batch cancel orders
/v2/order/cancel-all	POST	Cancel all orders
/v2/order/trade-list	GET	Query trade details
/v2/entrust/create-plan	POST	Create trigger order
/v2/entrust/create-profit	POST	Create take-profit/stop-loss
/v2/entrust/plan-list	GET	Query current trigger orders
/v2/entrust/plan-list-history	GET	Query historical trigger orders
/v2/entrust/plan-detail	GET	Query trigger order by ID
/v2/entrust/profit-list	GET	Query current take-profit/stop-loss orders
/v2/entrust/profit-detail	GET	Query take-profit/stop-loss by ID
/v2/entrust/cancel-plan	POST	Cancel trigger order
/v2/entrust/cancel-profit-stop	POST	Cancel take-profit/stop-loss
/v2/entrust/update-profit-stop	POST	Modify take-profit/stop-loss
/v2/entrust/cancel-all-plan	POST	Cancel all trigger orders
/v2/entrust/cancel-all-profit-stop	POST	Cancel all take-profit/stop-loss orders
/v2/order-entrust/list	GET	Query all orders and entrusts
/v2/order-entrust/cancel	POST	Cancel order or entrust
/v2/order-entrust/cancel-all	POST	Cancel all orders and entrusts
/v2/position/list	GET	Get position information
/v2/position/adjust-leverage	POST	Adjust leverage
/v2/position/margin	POST	Modify isolated margin
/v2/position/auto-margin	POST	Modify auto-add margin
/v2/position/close-all	POST	Close all positions
/v2/position/merge	POST	Merge positions
/v2/position/change-type	POST	Change position mode
/v2/position/confs	GET	Get position configuration
/v2/position/history/detail	GET	Get history position detail
/v2/position/history/async	GET	Async export history positions
/v2/system/user/info	GET	Get current API user info
/v2/system/download	GET	Download async export file by downloadId
3. Authentication
3.1 Apply for API Key
Please contact the OneBullEx official team to apply for API credentials:

Email: it@onebullex.com
Website: https://www.onebullex.com
3.2 V2 Authentication
All private endpoints (paths not starting with /v2/public/) require the following headers:

Header Name	Required	Description
X-API-KEY	Yes	API Access Key assigned by the platform
X-Signature	Yes	Request signature, see signature algorithm
X-Nonce	Yes	Random string, unique per request, prevents replay attacks
X-Timestamp	Yes	Current timestamp (seconds)
Public endpoints (paths starting with /v2/public/) do not require authentication.

Note on timestamp units: X-Timestamp uses a second-level timestamp and must be within 30 seconds of the server time, otherwise timestamp-error is returned. The Get Server Time endpoint, however, returns a millisecond-level timestamp — divide it by 1000 when using it to synchronise your clock.

X-Nonce must be unique per request; the server caches used nonces within the time window to prevent replay.

3.3 V2 Signature Algorithm
Step 1 -- Construct Parameter Set

Always include: nonce (from Header X-Nonce), timestamp (from Header X-Timestamp)
GET Requests: Add all query parameters to the set
POST Requests (JSON Body): Parse the JSON body, add top-level primitive fields (strings, numbers) to the set, ignore null values and nested objects/arrays
Step 2 -- Sort by Key in Lexicographic Order

Sort all parameters by key in ASCII lexicographic ascending order.

Step 3 -- Concatenate Signature String

key1=value1&key2=value2&key3=value3
Copy to clipboardErrorCopied
Numeric types: integers remain in integer form, decimals retain original precision (no scientific notation).

Step 4 -- HMAC-SHA256 Signature

Use the platform-assigned Secret Key to compute HMAC-SHA256 on the signature string, represent the result as a hexadecimal string, and set it in the X-Signature header.

GET Request Signature Example:

Request: GET /v2/public/q/ticker?symbol=btc_usdt&timeRangeType=UTC_P_8

Headers:
  X-API-KEY: your_access_key
  X-Nonce: abc123xyz
  X-Timestamp: 1711900000
  X-Signature: <HMAC-SHA256 result>

Signature string (sorted):
  nonce=abc123xyz&symbol=btc_usdt&timeRangeType=UTC_P_8&timestamp=1711900000
Copy to clipboardErrorCopied
POST Request Signature Example:

Request: POST /v2/order/create
Body: {"symbol":"btc_usdt","orderSide":"BUY","price":"50000","origQty":"1","orderType":"LIMIT","positionSide":"LONG","timeInForce":"GTC"}

Headers:
  X-API-KEY: your_access_key
  X-Nonce: def456uvw
  X-Timestamp: 1711900000
  X-Signature: <HMAC-SHA256 result>

Signature string (sorted):
  nonce=def456uvw&orderSide=BUY&orderType=LIMIT&origQty=1&positionSide=LONG&price=50000&symbol=btc_usdt&timeInForce=GTC&timestamp=1711900000
Copy to clipboardErrorCopied
3.4 V2 Unified Response Format
{
  "code": 0,
  "msg": "success",
  "data": {}
}
Copy to clipboardErrorCopied
Field	Type	Description
code	int	0 indicates success, non-0 indicates failure
msg	string	success on success, error code on failure
data	any	Business data, type varies by endpoint
See the full error code list in 7. Error Codes.

3.5 V2 Cursor Pagination
Some endpoints use cursor-based pagination. The response data structure is as follows:

Field	Type	Description
items	array	Data list
hasPrev	boolean	Whether a previous page is available
hasNext	boolean	Whether a next page is available
Pagination request parameters:

Parameter	Description
id	Cursor ID, omit for the first request, pass the id of the last record from the previous page for subsequent requests
direction	NEXT (next page) / PREV (previous page), default NEXT
limit	Number of records per page
4. Public Endpoints (V2)
Public endpoints do not require authentication and are used to retrieve public market data and contract information.

Base URL:

Test Environment: https://futures-openapi.1bullex.com
Production Environment: https://futures-openapi.onebullex.com
4.1 Server Time
GET /v2/public/time -- Get Server Time
Request Parameters: None

Response Example:

{
  "code": 0,
  "msg": "success",
  "data": 1711900000
}
Copy to clipboardErrorCopied
Field	Type	Description
data	long	Server current timestamp (milliseconds)
Note: this is a millisecond timestamp, whereas the X-Timestamp used for signing is in seconds — divide by 1000 before use.

4.2 Trading Pair Information
GET /v2/public/symbol/list -- Get All Trading Pair Configurations
Request Parameters: None

Response data: SymbolCacheDTO array

SymbolCacheDTO Field Definitions:

Field	Type	Description
symbol	string	Trading pair, e.g. btc_usdt
contractType	string	Contract type (perpetual, delivery)
underlyingType	string	Underlying type (coin-margined, USDT-margined)
contractSize	string	Contract multiplier (face value)
tradeSwitch	boolean	Trading pair switch
state	int	Status
initLeverage	int	Initial leverage
initPositionType	string	Initial position type
baseCoin	string	Base asset
quoteCoin	string	Quote asset
baseCoinPrecision	int	Base coin precision
baseCoinDisplayPrecision	int	Base coin display precision
quoteCoinPrecision	int	Quote coin precision
quoteCoinDisplayPrecision	int	Quote coin display precision
quantityPrecision	int	Quantity precision
pricePrecision	int	Price precision
supportOrderType	string	Supported order types
supportTimeInForce	string	Supported time-in-force types
supportEntrustType	string	Supported trigger order types
supportPositionType	string	Supported position types
minPrice	string	Minimum price
minQty	string	Minimum quantity
minNotional	string	Minimum notional value
maxNotional	string	Maximum notional value
multiplierDown	string	Limit sell order price lower bound percentage
multiplierUp	string	Limit buy order price upper bound percentage
maxOpenOrders	int	Maximum number of open orders
maxEntrusts	int	Maximum number of conditional orders
makerFee	string	Maker fee rate
takerFee	string	Taker fee rate
liquidationFee	string	Liquidation fee rate
marketTakeBound	string	Maximum price deviation for market orders
depthPrecisionMerge	int	Order book precision merge
labels	array<string>	Labels
onboardDate	long	Listing timestamp (milliseconds)
enName	string	Contract English name
cnName	string	Contract Chinese name
minStepPrice	string	Minimum price tick size
baseCoinName	string	Base coin name
quoteCoinName	string	Quote coin name
GET /v2/public/symbol/detail -- Get Single Trading Pair Configuration
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair, e.g. btc_usdt
Response data: SymbolCacheDTO, field definitions same as above.

GET /v2/public/symbol/coins -- Get Trading Pair Coin List
Request Parameters: None

Response Example:

{
  "code": 0,
  "msg": "success",
  "data": ["btc", "eth", "sol"]
}
Copy to clipboardErrorCopied
Field	Type	Description
data	array<string>	Available coin list
GET /v2/public/symbol/all -- Get All Trading Pair Names
Request Parameters: None

Response Example:

{
  "code": 0,
  "msg": "success",
  "data": ["btc_usdt", "eth_usdt", "sol_usdt"]
}
Copy to clipboardErrorCopied
Field	Type	Description
data	array<string>	All trading pair name list
4.3 Market Data Endpoints
GET /v2/public/q/ticker -- Get Ticker for a Specific Trading Pair
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
timeRangeType	query	string	Yes	Time zone type, e.g. H24
TimeRangeType:

Type	Description
H24	24 hours
UTC_P_12	utc+12
UTC_P_11	utc+11
UTC_P_10	
UTC_P_9	
UTC_P_8	
UTC_P_7	
UTC_P_6	
UTC_P_5	
UTC_P_4	
UTC_P_3	
UTC_P_2	
UTC_P_1	utc+1
UTC_P_0	utc+0
UTC_N_1	utc-1
UTC_N_2	
UTC_N_3	
UTC_N_4	
UTC_N_5	
UTC_N_6	
UTC_N_7	
UTC_N_8	
UTC_N_9	
UTC_N_10	
UTC_N_11	utc-11
UTC_N_12	utc-12
Response data: TickerVO

Field	Type	Description
t	long	Timestamp (milliseconds)
s	string	Trading pair
c	string	Latest price
h	string	24h high
l	string	24h low
a	string	24h volume
v	string	24h turnover
o	string	First trade price 24h ago
r	string	24h price change percentage
GET /v2/public/q/tickers -- Get Tickers for All Trading Pairs
Request Parameters:

Parameter	Location	Type	Required	Description
timeRangeType	query	string	Yes	Time zone type
Response data: TickerVO array, field definitions same as above.

GET /v2/public/q/agg-ticker -- Get Aggregated Ticker for a Specific Trading Pair
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
timeRangeType	query	string	Yes	Time zone type
Response data: AggTickerVO

Field	Type	Description
t	long	Timestamp (milliseconds)
s	string	Trading pair
c	string	Latest price
h	string	24h high
l	string	24h low
a	string	24h volume
v	string	24h turnover
o	string	First trade price 24h ago
r	string	24h price change percentage
i	string	Index price
m	string	Mark price
bp	string	Best bid price
ap	string	Best ask price
GET /v2/public/q/agg-tickers -- Get Aggregated Tickers for All Trading Pairs
Request Parameters:

Parameter	Location	Type	Required	Description
timeRangeType	query	string	Yes	Time zone type
Response data: AggTickerVO array, field definitions same as above.

GET /v2/public/q/depth -- Get Order Book Depth
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
level	query	int	Yes	Depth level, range 1~50
Response data: DepthVO

Field	Type	Description
t	long	Timestamp (milliseconds)
s	string	Trading pair
u	long	updateId
b	array<string[]>	Bid list, each item is [price, quantity]
a	array<string[]>	Ask list, each item is [price, quantity]
GET /v2/public/q/deal -- Get Latest Trades
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
num	query	long	No	Number of records to return, default 50, minimum 1
Response data: DealVO array

Field	Type	Description
t	long	Trade timestamp (milliseconds)
s	string	Trading pair
p	string	Trade price
a	string	Trade volume
m	string	Trade side (BUY / SELL)
GET /v2/public/q/kline -- Get K-Line Data
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
interval	query	string	Yes	Time interval, e.g. 1m, 5m, 1h, 1d
startTime	query	long	No	Start timestamp (milliseconds)
endTime	query	long	No	End timestamp (milliseconds)
limit	query	int	No	Number of records, default 500, range 1~1500
Response data: KlineVO array

Field	Type	Description
s	string	Trading pair
t	long	Timestamp (milliseconds)
o	string	Open price
c	string	Close price
h	string	High price
l	string	Low price
a	string	Volume
v	string	Turnover
GET /v2/public/q/mark-price -- Get Mark Price
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	No	Trading pair, returns all trading pairs if omitted
Response data: PriceVO array

Field	Type	Description
s	string	Trading pair
p	string	Mark price
t	long	Timestamp (milliseconds)
GET /v2/public/q/symbol-mark-price -- Get Mark Price for a Single Trading Pair
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
Response data: PriceVO, field definitions same as above.

GET /v2/public/q/index-price -- Get Index Price
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	No	Trading pair, returns all trading pairs if omitted
Response data: PriceVO array, field definitions same as above.

GET /v2/public/q/symbol-index-price -- Get Index Price for a Single Trading Pair
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
Response data: PriceVO, field definitions same as above.

GET /v2/public/q/funding-rate -- Get Funding Rate
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
Response data: FundRateVO

Field	Type	Description
symbol	string	Trading pair
fundingRate	string	Current funding rate
nextCollectionTime	long	Next collection timestamp (milliseconds)
GET /v2/public/q/funding-rate-record -- Get Funding Rate History
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
id	query	long	No	Cursor ID
direction	query	string	No	PREV / NEXT, default NEXT
limit	query	int	No	Records per page, default 10
Response data: Cursor pagination, items is FundRateRecordVO array

Field	Type	Description
id	string	Record ID
symbol	string	Trading pair
fundingRate	string	Funding rate
createdTime	long	Timestamp (milliseconds)
collectionInterval	long	Collection interval (seconds)
collectionInternal	long	Deprecated alias of collectionInterval
4.4 Contract Information
GET /v2/public/contract/risk-balance -- Get Insurance Fund Balance Records
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
id	query	long	No	Cursor ID
direction	query	string	No	PREV / NEXT, default NEXT
limit	query	int	No	Records per page, default 10
Response data: Cursor pagination, items is RiskBalanceVO array

Field	Type	Description
id	string	Record ID
coin	string	Coin
amount	string	Insurance fund balance
createdTime	long	Timestamp (milliseconds)
GET /v2/public/contract/open-interest -- Get Open Interest for a Trading Pair
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
Response data: OpenInterestVO

Field	Type	Description
symbol	string	Trading pair
openInterest	string	Open interest (contracts)
openInterestUsd	string	Open interest value (USD)
time	long	Timestamp (milliseconds)
4.5 Leverage Brackets
GET /v2/public/leverage/bracket/list -- Get Leverage Brackets for All Trading Pairs
Request Parameters: None

Response data: SymbolBracketVO array

Field	Type	Description
symbol	string	Trading pair
leverageBrackets	array	Bracket list, see LeverageBracketVO
LeverageBracketVO Field Definitions:

Field	Type	Description
symbol	string	Trading pair
bracket	int	Bracket level number
maxNominalValue	string	Maximum notional value for this bracket
maintMarginRate	string	Maintenance margin rate
startMarginRate	string	Initial margin rate
maxStartMarginRate	string	Maximum initial margin rate
maxLeverage	string	Maximum leverage
minLeverage	string	Minimum leverage
GET /v2/public/leverage/bracket/detail -- Get Leverage Brackets for a Single Trading Pair
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
Response data: SymbolBracketVO, field definitions same as above.

5. Private Endpoints (V2)
Private endpoints require authentication and are used for futures trading, fund management, and position operations.

Base URL:

Test Environment: https://futures-openapi.1bullex.com
Production Environment: https://futures-openapi.onebullex.com
Authentication: See 3.3 V2 Authentication and 3.4 V2 Signature Algorithm

All private endpoint requests must include headers: X-API-KEY, X-Signature, X-Nonce, X-Timestamp

5.1 WebSocket Subscription
GET /v2/user/listen-key -- Get ListenKey
Request Parameters: None

Response Example:

{
  "code": 0,
  "msg": "success",
  "data": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
Copy to clipboardErrorCopied
Field	Type	Description
data	string	ListenKey, used to establish WebSocket private channel connection
5.2 Fund Account
GET /v2/balance/list -- Get All User Balances
Request Parameters: None

Response data: BalanceVO array

Field	Type	Description
coin	string	Coin
walletBalance	string	Wallet balance
openOrderMarginFrozen	string	Order frozen margin
isolatedMargin	string	Isolated margin frozen
crossedMargin	string	Cross initial margin
availableBalance	string	Available balance
bonus	string	Bonus balance
Available balance = Wallet balance - Isolated margin - Cross margin - Order frozen margin

GET /v2/balance/detail -- Get Single Coin Balance
Request Parameters:

Parameter	Location	Type	Required	Description
coin	query	string	Yes	Coin, e.g. USDT
Response data: BalanceVO, field definitions same as above.

GET /v2/balance/bills -- Get Account Transaction Records
Request Parameters:

Parameter	Location	Type	Required	Description
coin	query	string	No	Coin filter
symbol	query	string	No	Trading pair filter
type	query	string	No	Transaction type filter
startTime	query	long	No	Start timestamp (milliseconds)
endTime	query	long	No	End timestamp (milliseconds)
id	query	long	No	Cursor ID
direction	query	string	No	PREV / NEXT, default NEXT
limit	query	int	No	Records per page, default 10
Response data: Cursor pagination, items is BalanceBillVO array

Field	Type	Description
id	string	Transaction record ID
coin	string	Coin
symbol	string	Trading pair (if applicable)
type	string	Transaction type. Common values: EXCHANGE (transfer) / CLOSE_POSITION (close position P&L) / TAKE_OVER (position takeover) / QIANG_PING_MANAGER (liquidation management fee) / FUND (funding fee) / FEE (trading fee) / ADL (auto-deleveraging) / MERGE (position merge). This list is not exhaustive; other values may appear for bonus, referral, or copy-trading related transactions.
amount	string	Change amount
side	string	Change direction: ADD (deposit) / SUB (withdrawal)
afterAmount	string	Balance after change
createdTime	long	Timestamp (milliseconds)
GET /v2/balance/funding -- Get Funding Account(USDT) Balance
Request Parameters: None

Response data: FundingAccountVO

Field	Type	Description
balance	decimal	Balance
frozen	decimal	Frozen amount
available	decimal	Available amount
POST /v2/balance/transfer -- Account Transfer
Request Body (JSON):

Field	Type	Required	Description
billNo	string	Yes	Idempotency key, must be unique per request
from	string	Yes	Source account type: FUNDING (funding account) / CONTRACT (contract account)
to	string	Yes	Destination account type: FUNDING (funding account) / CONTRACT (contract account)
amount	decimal	Yes	Transfer amount, must be greater than 0
remark	string	No	Remark
from and to cannot be the same.

Response data: Transfer record code (long, returned as string)

GET /v2/bot/redeeming-info — Retrieve Redemption Queue Summary
Request Parameters: None

Response data: BotRedeemingInfo

Field	Type	Description
estimatedAmount	string	Current redemption amount in the queue
pendingCount	long	Current number of pending redemption requests
5.3 Order Management
POST /v2/order/create -- Place Order
Note: After placing an order through this interface and obtaining the order ID, you need to use the Query Order Details by ID interface to obtain the order details information to determine whether the order was successfully executed. Because our platform is an asynchronous system, there may be a delay in obtaining order information in special circumstances. If you encounter this situation, you SHOULD NOT simply assume that the order has failed. You should query the order details multiple times to confirm the order execution status. If the problem is frequent or persistent, please contact our platform customer service in time.

Request Body (JSON):

Field	Type	Required	Description
symbol	string	Yes	Trading pair
orderType	string	Yes	Order type: LIMIT / MARKET
orderSide	string	Yes	Order side: BUY / SELL
positionSide	string	Yes	Position side: LONG / SHORT
origQty	decimal	Yes	Order quantity (contracts), must be greater than 0
price	decimal	Conditional	Order price, required when orderType=LIMIT. See constraint 1 below
timeInForce	string	No	Time in force: GTC / IOC / FOK / GTX. Allowed values depend on orderType. See constraint 2 below
reduceOnly	boolean	No	Whether reduce-only, default false
clientOrderId	string	No	Custom order ID, length 1~32, supports alphanumeric and _.-
positionId	long	No	Position ID when closing a position. See constraint 3 below
leverage	int	No	Leverage
triggerProfitPrice	decimal	Conditional	Take-profit trigger price. See constraints 4 and 5 below
triggerStopPrice	decimal	Conditional	Stop-loss trigger price. See constraints 4 and 5 below
profitOrderType	string	No	Take-profit order type: MARKET / LIMIT, default MARKET
stopOrderType	string	No	Stop-loss order type: MARKET / LIMIT, default MARKET
profitOrderPrice	decimal	Conditional	Take-profit order price, required when profitOrderType=LIMIT. See constraint 5 below
stopOrderPrice	decimal	Conditional	Stop-loss order price, required when stopOrderType=LIMIT. See constraint 5 below
marketOrderLevel	int	No	Market order best level: 1 (counterparty price) / 5 / 10 / 15
Field constraints:

The following fields are declared optional, but must be supplied under specific conditions; otherwise the request is rejected.

price: Required when orderType=LIMIT. The price scale must not exceed the symbol's pricePrecision and the price must be a multiple of the symbol's minStepPrice, otherwise invalid_price is returned. Ignored when orderType=MARKET.
timeInForce: When omitted, it defaults based on orderType — IOC for MARKET, GTC for LIMIT. When supplied explicitly with orderType=MARKET, only IOC or FOK are accepted; GTC / GTX return invalid_time_in_force.
positionId: Recommended for close-direction orders (LONG+SELL, or SHORT+BUY). Once a value greater than 0 is supplied, the position must belong to the current account and match symbol, otherwise invalid_params is returned.
triggerProfitPrice / triggerStopPrice: Both are optional, but supplying either one turns the request into an order with attached take-profit/stop-loss, and every TP/SL constraint in item 5 then applies. If neither is supplied, no TP/SL is created.
Pairing rules for TP/SL fields:
When profitOrderType=LIMIT, triggerProfitPrice and profitOrderPrice must both be present or both be absent; supplying only one returns invalid_params.
When stopOrderType=LIMIT, the same pairing rule applies to triggerStopPrice and stopOrderPrice.
profitOrderType / stopOrderType default to MARKET when omitted, in which case the corresponding order price is not needed.
Trigger prices and order prices are subject to the same pricePrecision and minStepPrice constraints.
Trigger price direction (long = BUY with LONG, short = SELL with SHORT): for a long, the take-profit trigger must not be below the order price (trigger_profit_price_less_than_entry_price) and the stop-loss trigger must not be above it (trigger_stop_price_more_than_entry_price); for a short the directions are reversed. In addition, a long's stop-loss trigger must be strictly below the current best ask (trigger_stop_price_must_less_than_ask_price), and a short's strictly above the current best bid (trigger_stop_price_must_more_than_bid_price).
If profitOrderType or stopOrderType is MARKET and the order itself is a market order (no price supplied), the symbol's latest traded price is used for the checks above; if that price is unavailable, invalid_price is returned.
origQty must be a whole number of contracts; any decimal places return invalid_quantity.

Response data: Order ID (long, returned as string)

POST /v2/order/create-batch -- Batch Place Orders
Request Body (JSON):

Field	Type	Required	Description
list	string	Yes	JSON string of order array, each element has the same fields as the place order endpoint
Response data: boolean, true indicates success

GET /v2/order/listUnfinished -- Query Current Open Orders (Single Trading Pair)
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
direction	query	string	Yes	Direction: BUY / SELL
Response data: OrderVO array, field definitions see below.

GET /v2/order/all/listUnfinished -- Query Current Open Orders (Multiple Trading Pairs)
Request Parameters:

Parameter	Location	Type	Required	Description
list	query	string	Yes	Trading pair list, comma-separated, e.g. btc_usdt,eth_usdt
Response data: OrderVO array, field definitions see below.

GET /v2/order/list -- Query Order List (Paginated)
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	No	Trading pair
status	query	string	No	Order status filter
page	query	int	No	Page number, default 1
size	query	int	No	Records per page
Response data: Paginated result, items is OrderVO array, field definitions see below.

POST /v2/order/list-by-ids -- Query Orders by ID List
Request Body (JSON):

Field	Type	Required	Description
ids	array<long>	Yes	Order ID list
Response data: OrderVO array, field definitions see below.

GET /v2/order/list-history -- Query Historical Orders
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	No	Trading pair
startTime	query	long	No	Start timestamp (milliseconds)
endTime	query	long	No	End timestamp (milliseconds)
id	query	long	No	Cursor ID
direction	query	string	No	PREV / NEXT, default NEXT
limit	query	int	No	Records per page
forceClose	query	boolean	No	Whether to query liquidation orders, default false
Response data: Cursor pagination, items is OrderVO array, field definitions see below.

GET /v2/order/detail -- Query Order Details by ID
Request Parameters:

Parameter	Location	Type	Required	Description
orderId	query	long	Yes	Order ID
Response data: OrderVO, field definitions see below.

OrderVO Field Definitions:

Field	Type	Description
orderId	string	Order ID
positionId	long	Position ID
clientOrderId	string	Custom order ID
symbol	string	Trading pair
orderType	string	Order type: LIMIT / MARKET
orderSide	string	Order side: BUY / SELL
positionSide	string	Position side: LONG / SHORT
timeInForce	string	Time in force
closePosition	boolean	Whether conditional close-all
price	string	Order price
origQty	string	Order quantity (contracts)
avgPrice	string	Average fill price
executedQty	string	Filled quantity (contracts)
marginFrozen	string	Frozen margin
triggerProfitPrice	string	Take-profit trigger price
triggerStopPrice	string	Stop-loss trigger price
sourceId	long	Conditional trigger ID
forceClose	boolean	Whether liquidation order
closeProfit	string	Close position P&L
state	string	Order status: NEW (unfilled) / PARTIALLY_FILLED (partially filled) / PARTIALLY_CANCELED (partially canceled) / FILLED (fully filled) / CANCELED (canceled) / REJECTED (rejected) / EXPIRED (expired)
createdTime	long	Creation timestamp (milliseconds)
POST /v2/order/cancel -- Cancel Order
Request Body (JSON):

Field	Type	Required	Description
orderId	long	Yes	Order ID
Response data: Cancellation result

POST /v2/order/cancel-batch -- Batch Cancel Orders
Request Body (JSON):

Field	Type	Required	Description
orderIds	string	Yes	JSON string of order ID array, e.g. "[123456,789012]"
Response data: boolean, true indicates success

POST /v2/order/cancel-all -- Cancel All Orders
Request Body (JSON):

Field	Type	Required	Description
symbol	string	No	Trading pair, cancels all trading pair orders if omitted
Response data: boolean, true indicates success

GET /v2/order/trade-list -- Query Trade Details
Request Parameters:

Parameter	Location	Type	Required	Description
orderId	query	long	No	Order ID
symbol	query	string	No	Trading pair
startTime	query	long	No	Start timestamp (milliseconds)
endTime	query	long	No	End timestamp (milliseconds)
page	query	int	No	Page number, default 1, minimum 1
size	query	int	No	Records per page, default 10, maximum 100
Response data: Paginated result, items is OrderTradeVO array

Field	Type	Description
orderId	string	Order ID
execId	string	Trade ID
symbol	string	Trading pair
quantity	string	Trade quantity
price	string	Trade price
fee	string	Trading fee
feeCoin	string	Fee coin
timestamp	long	Trade timestamp (milliseconds)
5.4 Trigger Orders and Take-Profit/Stop-Loss
POST /v2/entrust/create-plan -- Create Trigger Order
Request Body (JSON):

Field	Type	Required	Description
symbol	string	Yes	Trading pair
orderSide	string	Yes	Order side: BUY / SELL
positionSide	string	Yes	Position side: LONG / SHORT
entrustType	string	Yes	Entrust type: STOP (limit) / STOP_MARKET (market)
timeInForce	string	Yes	Time in force: GTC / IOC / FOK / GTX
triggerPriceType	string	Yes	Trigger price type: MARK_PRICE / LATEST_PRICE
origQty	decimal	Yes	Order quantity (contracts), must be greater than 0
stopPrice	decimal	Conditional	Trigger price; effectively required. See constraint 1 below
price	decimal	Conditional	Order price, required when entrustType=STOP. See constraint 2 below
positionId	string	Conditional	Position ID, required for close-direction entrusts. See constraint 3 below
marketOrderLevel	int	No	Market order best level: 1 (counterparty price) / 5 / 10 / 15
expireTime	long	No	Expiration timestamp (milliseconds)
Field constraints:

The following fields are declared optional, but must be supplied under specific conditions; otherwise the request is rejected.

stopPrice: Although marked optional, the server requires it for every trigger order; omitting it returns invalid_params. The value must be a multiple of the symbol's minStepPrice, otherwise invalid_stop_price is returned.
price: Required when entrustType=STOP (limit), and must satisfy the pricePrecision and minStepPrice constraints, otherwise invalid_price is returned. Not needed when entrustType=STOP_MARKET (market). When both price and stopPrice are supplied, their deviation is capped by the symbol: for BUY, price must not exceed stopPrice × (1 + multiplierUp) (price_cannot_greater_than_stop_price_of); for SELL, price must not fall below stopPrice × (1 - multiplierDown) (price_cannot_less_than_stop_price_of).
positionId: Required for close-direction trigger orders, i.e. orderSide=BUY with positionSide=SHORT, or orderSide=SELL with positionSide=LONG. Such requests without positionId return invalid_params.
origQty must be a whole number of contracts; any decimal places return invalid_quantity_scale.

Response data: Entrust ID

POST /v2/entrust/create-profit -- Create Take-Profit/Stop-Loss
Request Body (JSON):

Field	Type	Required	Description
symbol	string	Yes	Trading pair
origQty	decimal	Yes	Order quantity (contracts), 0 means trigger by full position
positionSide	string	Conditional	Position side: LONG / SHORT, required when positionId is omitted. See constraint 2 below
orderSide	string	Conditional	Order side: BUY / SELL, required when positionId is omitted. See constraint 2 below
triggerPriceType	string	No	Trigger price type: MARK_PRICE / LATEST_PRICE, default LATEST_PRICE
triggerProfitPrice	decimal	Conditional	Take-profit trigger price; at least one of this and triggerStopPrice is required. See constraints 1 and 3 below
triggerStopPrice	decimal	Conditional	Stop-loss trigger price; at least one of this and triggerProfitPrice is required. See constraints 1 and 3 below
profitOrderType	string	No	Take-profit order type: MARKET / LIMIT, default MARKET
stopOrderType	string	No	Stop-loss order type: MARKET / LIMIT, default MARKET
profitOrderPrice	decimal	Conditional	Take-profit order price, required when profitOrderType=LIMIT. See constraint 3 below
stopOrderPrice	decimal	Conditional	Stop-loss order price, required when stopOrderType=LIMIT. See constraint 3 below
positionId	string	No	Position ID; supplying it or not selects one of two modes. See constraint 2 below
reduceOnly	boolean	No	Whether reduce-only, default true; forced to true when positionId is supplied (close-position TP/SL)
profitFlag	int	No	1 (full take-profit/stop-loss) / 2 (partial take-profit/stop-loss); 0 or 1 is treated as 1, any other value as 2
expireTime	long	No	Expiration timestamp (milliseconds)
Field constraints:

The following fields are declared optional, but must be supplied under specific conditions; otherwise the request is rejected.

triggerProfitPrice / triggerStopPrice: These cannot both be empty — at least one must be supplied, otherwise invalid_params is returned. You may set take-profit only, stop-loss only, or both.
positionId selects one of two modes:
positionId omitted (open-position TP/SL): orderSide and positionSide are both required and must be valid enum values (orderSide is BUY / SELL, positionSide is LONG / SHORT). A missing or invalid value returns invalid_params.
positionId supplied (close-position TP/SL): positionSide is taken from the actual direction of that position (LONG / SHORT) and the value in the request is ignored; the closing side is derived from the position direction (LONG → SELL, SHORT → BUY), so orderSide need not be supplied. The position must belong to the current account and match symbol; origQty must not exceed the closable size of that position, otherwise more_than_available is returned.
Pairing rules for TP/SL fields:
When profitOrderType=LIMIT, triggerProfitPrice and profitOrderPrice must both be present or both be absent; supplying only one returns invalid_params.
When stopOrderType=LIMIT, the same pairing rule applies to triggerStopPrice and stopOrderPrice.
profitOrderType / stopOrderType default to MARKET, in which case the corresponding order price is not needed.
All trigger and order prices must not exceed the symbol's pricePrecision and must be multiples of minStepPrice, otherwise invalid_trigger_profit_price / invalid_trigger_stop_price / invalid_params is returned.
Trigger price direction: when the closing side is SELL (a long position), the take-profit trigger must not be below the current price and the stop-loss trigger must not be above it; when the closing side is BUY (a short position), the directions are reversed. The corresponding error codes are trigger_profit_price_less_than_current_price, trigger_profit_price_more_than_current_price, trigger_stop_price_more_than_current_price, and trigger_stop_price_less_than_current_price. The "current price" comes from the source selected by triggerPriceType.
origQty must be a non-negative whole number of contracts: decimal places return invalid_quantity_scale and negative values return quantity_can_not_less_than; 0 means the full position size is closed when triggered.

Response data: Take-profit/stop-loss ID

GET /v2/entrust/plan-list -- Query Current Trigger Orders
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	No	Trading pair
page	query	int	No	Page number
size	query	int	No	Records per page
Response data: Paginated result, items is PlanEntrustVO array, field definitions see below.

GET /v2/entrust/plan-list-history -- Query Historical Trigger Orders
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	No	Trading pair
startTime	query	long	No	Start timestamp (milliseconds)
endTime	query	long	No	End timestamp (milliseconds)
id	query	long	No	Cursor ID
direction	query	string	No	PREV / NEXT, default NEXT
limit	query	int	No	Records per page
Response data: Cursor pagination, items is PlanEntrustVO array, field definitions see below.

GET /v2/entrust/plan-detail -- Query Trigger Order by ID
Request Parameters:

Parameter	Location	Type	Required	Description
entrustId	query	long	Yes	Trigger order ID
Response data: PlanEntrustVO, field definitions see below.

PlanEntrustVO Field Definitions:

Field	Type	Description
entrustId	string	Entrust ID
symbol	string	Trading pair
entrustType	string	Entrust type: STOP (limit) / STOP_MARKET (market)
orderSide	string	Order side: BUY / SELL
positionSide	string	Position side: LONG / SHORT
timeInForce	string	Time in force
closePosition	boolean	Whether trigger close-all
price	string	Order price
origQty	string	Order quantity (contracts)
stopPrice	string	Trigger price
triggerPriceType	string	Trigger price type
isOrdinary	boolean	Whether ordinary trigger order
state	string	Status: NOT_TRIGGERED / TRIGGERING / TRIGGERED / USER_REVOCATION (user canceled) / PLATFORM_REVOCATION (platform canceled) / EXPIRED
marketOrderLevel	int	Market order best level
createdTime	long	Creation timestamp (milliseconds)
GET /v2/entrust/profit-list -- Query Current Take-Profit/Stop-Loss Orders
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	No	Trading pair
page	query	int	No	Page number
size	query	int	No	Records per page
Response data: Paginated result, items is ProfitEntrustVO array, field definitions see below.

GET /v2/entrust/profit-detail -- Query Take-Profit/Stop-Loss by ID
Request Parameters:

Parameter	Location	Type	Required	Description
profitId	query	long	Yes	Take-profit/stop-loss ID
Response data: ProfitEntrustVO, field definitions see below.

ProfitEntrustVO Field Definitions:

Field	Type	Description
profitId	string	Entrust ID
symbol	string	Trading pair
positionSide	string	Position side: LONG / SHORT
origQty	string	Order quantity (contracts)
triggerPriceType	string	Trigger price type: MARK_PRICE / LATEST_PRICE
triggerProfitPrice	string	Take-profit trigger price
triggerStopPrice	string	Stop-loss trigger price
entryPrice	string	Entry average price
positionSize	string	Position size (contracts)
isolatedMargin	string	Isolated margin
executedQty	string	Actual filled quantity
state	string	Status: NOT_TRIGGERED / TRIGGERING / TRIGGERED / USER_REVOCATION (user canceled) / PLATFORM_REVOCATION (platform canceled) / EXPIRED
createdTime	long	Creation timestamp (milliseconds)
POST /v2/entrust/cancel-plan -- Cancel Trigger Order
Request Body (JSON):

Field	Type	Required	Description
entrustId	long	Yes	Trigger order ID
Response data: Cancellation result

POST /v2/entrust/cancel-profit-stop -- Cancel Take-Profit/Stop-Loss
Request Body (JSON):

Field	Type	Required	Description
profitId	long	Yes	Take-profit/stop-loss ID
Response data: Cancellation result

POST /v2/entrust/update-profit-stop -- Modify Take-Profit/Stop-Loss
Request Body (JSON):

Field	Type	Required	Description
profitId	long	Yes	Take-profit/stop-loss ID
triggerProfitPrice	decimal	Conditional	New take-profit trigger price; at least one of this and triggerStopPrice is required. See constraint 1 below
triggerStopPrice	decimal	Conditional	New stop-loss trigger price; at least one of this and triggerProfitPrice is required. See constraint 1 below
profitOrderPrice	decimal	Conditional	New take-profit order price, required when profitOrderType=LIMIT. See constraint 2 below
stopOrderPrice	decimal	Conditional	New stop-loss order price, required when stopOrderType=LIMIT. See constraint 2 below
Field constraints:

triggerProfitPrice / triggerStopPrice: These cannot both be empty — at least one must be supplied, otherwise invalid_params is returned. Trigger prices are subject to the original symbol's pricePrecision and minStepPrice constraints and to the same direction checks as on creation.
Pairing rules for the order prices: Same as Create Take-Profit/Stop-Loss — when profitOrderType=LIMIT, triggerProfitPrice and profitOrderPrice must both be present or both be absent; the same applies to triggerStopPrice and stopOrderPrice when stopOrderType=LIMIT. An invalid type value returns invalid_params.
Response data: Modification result

POST /v2/entrust/cancel-all-plan -- Cancel All Trigger Orders
Request Body (JSON):

Field	Type	Required	Description
symbol	string	No	Trading pair, cancels all trading pair trigger orders if omitted
Response data: boolean, true indicates success

POST /v2/entrust/cancel-all-profit-stop -- Cancel All Take-Profit/Stop-Loss Orders
Request Body (JSON):

Field	Type	Required	Description
symbol	string	No	Trading pair, cancels all trading pair take-profit/stop-loss orders if omitted
Response data: boolean, true indicates success

5.5 All Orders and Entrusts
GET /v2/order-entrust/list -- Query All Orders and Entrusts
Request Parameters:

Parameter	Location	Type	Required	Description
type	query	string	No	Entrust type: ORDER (limit/market order, default) / ENTRUST (trigger order)
symbol	query	string	No	Trading pair
page	query	int	No	Page number
size	query	int	No	Records per page
Response data: Paginated result, items is OrderEntrustVO array

OrderEntrustVO Field Definitions:

Field	Type	Description
id	string	Entrust ID (order ID or trigger order ID)
type	string	Type: ORDER / ENTRUST
symbol	string	Trading pair
orderType	string	Order type
orderSide	string	Order side: BUY / SELL
positionSide	string	Position side: LONG / SHORT
timeInForce	string	Time in force
closePosition	boolean	Whether conditional close-all
price	string	Order price
origQty	string	Order quantity (contracts)
avgPrice	string	Average fill price
executedQty	string	Filled quantity (contracts)
marginFrozen	string	Frozen margin
triggerProfitPrice	string	Take-profit trigger price
triggerStopPrice	string	Stop-loss trigger price
leverage	int	Leverage
entrustOrderId	long	Conditional trigger ID
closeProfit	string	Close position P&L
state	string	Status: NEW / PARTIALLY_FILLED / FILLED / CANCELED / REJECTED / EXPIRED
createdTime	long	Creation timestamp (milliseconds)
entrustType	string	Trigger order type (has value when type=ENTRUST)
stopPrice	string	Trigger price (has value when type=ENTRUST)
triggerPriceType	string	Trigger price type (has value when type=ENTRUST)
isOrdinary	boolean	Whether ordinary trigger order (has value when type=ENTRUST)
marketOrderLevel	int	Market order best level
forceClose	boolean	Whether liquidation
POST /v2/order-entrust/cancel -- Cancel Order or Entrust
Request Body (JSON):

Field	Type	Required	Description
type	string	Yes	Entrust type: ORDER / ENTRUST
id	long	Yes	Entrust ID
Response data: Cancellation result

POST /v2/order-entrust/cancel-all -- Cancel All Orders and Entrusts
Request Body (JSON):

Field	Type	Required	Description
symbol	string	No	Trading pair, cancels all trading pair orders and trigger orders if omitted
Response data: boolean, true indicates success

5.6 Position Management
GET /v2/position/list -- Get Position Information
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	No	Trading pair, returns all positions if omitted
Response data: PositionVO array

Field	Type	Description
symbol	string	Trading pair
positionId	string	Position ID
positionType	string	Position type: CROSSED (cross margin) / ISOLATED (isolated margin)
positionSide	string	Position side: LONG / SHORT
positionSize	string	Position size (contracts)
closeOrderSize	string	Close order quantity (contracts)
availableCloseSize	string	Available close quantity (contracts)
entryPrice	string	Entry average price
isolatedMargin	string	Isolated margin
openOrderMarginFrozen	string	Open order margin frozen
realizedProfit	string	Realized P&L
autoMargin	boolean	Whether auto-add margin is enabled
leverage	int	Leverage
contractSize	string	Contract multiplier
liqPrice	string	Estimated liquidation price; 0 when not applicable
POST /v2/position/adjust-leverage -- Adjust Leverage
Request Body (JSON):

Field	Type	Required	Description
symbol	string	Yes	Trading pair
leverage	int	Yes	Target leverage, minimum 1
Response data: Adjustment result

POST /v2/position/margin -- Modify Isolated Margin
Request Body (JSON):

Field	Type	Required	Description
symbol	string	Yes	Trading pair
positionSide	string	Yes	Position side: LONG / SHORT
positionId	long	Yes	Position ID
margin	decimal	Yes	Adjustment amount, must be greater than 0
type	string	Yes	Adjustment direction: ADD (increase) / SUB (decrease)
Response data: Adjustment result

POST /v2/position/auto-margin -- Modify Auto-Add Margin
Request Body (JSON):

Field	Type	Required	Description
symbol	string	Yes	Trading pair
positionSide	string	Yes	Position side: LONG / SHORT
autoMargin	boolean	Yes	Whether to enable auto-add margin
Response data: Modification result

POST /v2/position/close-all -- Close All Positions
Request Body (JSON):

Field	Type	Required	Description
symbol	string	No	Trading pair, closes all positions if omitted
Response data: Close result

POST /v2/position/merge -- Merge Positions
Request Body (JSON):

Field	Type	Required	Description
symbol	string	Yes	Trading pair
Response data: Merge result

POST /v2/position/change-type -- Change Position Mode
Request Body (JSON):

Field	Type	Required	Description
symbol	string	Yes	Trading pair
positionType	string	Yes	Target position type: CROSSED (cross margin) / ISOLATED (isolated margin)
positionModel	string	Yes	Position model: AGGREGATION (one-way) / DISAGGREGATION (hedge)
Response data: Modification result

GET /v2/position/confs -- Get Position Configuration
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
Response data: PositionConfVO array

Field	Type	Description
symbol	string	Trading pair
positionType	string	Position type: CROSSED / ISOLATED
positionSide	string	Position side: LONG / SHORT
positionModel	string	Position model: DISAGGREGATION (hedge) / AGGREGATION (one-way)
autoMargin	bool	Automatic margin call
leverage	integer	Leverage
GET /v2/position/history/detail -- Get History Position Detail
Request Parameters:

Parameter	Location	Type	Required	Description
symbol	query	string	Yes	Trading pair
positionId	query	long	Yes	Position ID
Response data: PositionLogVO

Field	Type	Description
id	long	Position log ID
symbolId	int	Symbol ID
symbol	string	Trading pair
userId	long	User ID
accountId	long	Account ID
leverage	int	Leverage
positionType	string	Position type: CROSSED (cross margin) / ISOLATED (isolated margin)
positionSide	string	Position side: LONG / SHORT
positionModel	string	Position model: AGGREGATION (one-way) / DISAGGREGATION (hedge)
entryPrice	string	Entry price
closePrice	string	Close price
maxPositionSize	string	Maximum position size (contracts)
closeOrderSize	string	Close quantity (contracts)
realizedProfit	string	Realized P&L
tradeFee	string	Trading fee
profitRate	string	Profit rate
takeOver	boolean	Whether position was taken over (liquidation takeover)
createdTime	long	Creation timestamp (milliseconds)
updatedTime	long	Update timestamp (milliseconds)
finished	boolean	Whether the position log is finished (fully closed)
unsettledProfit	string	Unsettled profit
fundingFee	string	Funding fee
liqPrice	string	Liquidation price; 0 when not liquidated
GET /v2/position/history/async -- Async Export History Positions
Creates an async export task and returns downloadId synchronously. After the file is ready, download it via GET /v2/system/download.

Limits:

Interval between startTime and endTime must not exceed 1 year
Each account can create at most 5 history-position export tasks per calendar month
Request Parameters:

Parameter	Location	Type	Required	Description
startTime	query	long	Yes	Start timestamp (milliseconds)
endTime	query	long	Yes	End timestamp (milliseconds)
Response data: AsyncDownloadTaskVO

Field	Type	Description
downloadId	string	Download task ID for later download
5.7 System Services
GET /v2/system/user/info -- Get Current API User Info
Request Parameters: None

Response data: ApiUserInfoVO

Field	Type	Description
userId	long	Current API user identifier (from accountId)
GET /v2/system/download -- Download Async Export File by downloadId
OSS proxy download endpoint: returns the Excel file stream when the task succeeds; returns an error if the file is not ready or generation failed.

Limits: Each downloadId allows at most 5 successful downloads per hour.

Request Parameters:

Parameter	Location	Type	Required	Description
downloadId	query	string	Yes	Async export task ID
Success Response: file stream

Header	Description
Content-Type	application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition	attachment; filename="position_history_{downloadId}.xlsx"
Common Error Codes:

Error Code	Description
file_not_ready	File has not been generated yet
file_generate_failed	File generation failed
request count limit	Download rate limit exceeded
invalid_params	Invalid downloadId or not owned by current account
6. WebSocket API
6.1 Overview
This document describes the OBE trading platform Open WebSocket API access protocol, used to receive real-time pushes for account balances, order status, position information, price data, etc. This service is designed for API users, and all channels require authentication before subscription.

6.2 Connection Information
6.2.1 Connection URL
Test Environment: wss://openapi.1bullex.com/fstream/ws/open
Production Environment: wss://openapi.onebullex.com/fstream/ws/open
Copy to clipboardErrorCopied
Protocol: Standard WebSocket (WSS)
Supports text messages (JSON) and binary messages (UTF-8 encoded JSON)
A single connection can subscribe to multiple channels and multiple trading pairs simultaneously
6.2.2 Connection Lifecycle
Client initiates WebSocket connection
After connection is established, send subscription request (with signature authentication)
Server verifies signature and returns subscription result
Server pushes real-time data via binary messages
Server sends heartbeat ping every 15 seconds, client must reply with pong
If no pong response is received within 60 seconds, server actively disconnects
6.3 Authentication Mechanism
6.3.1 API Keys
You need to obtain an API key pair first: AccessKey and SecretKey
AccessKey: Used to identify the API user, set in the key field of the request
SecretKey: Used for signature verification, must be stored securely
API must have futures trading permission enabled (contractTrade = true)
6.3.2 Signature Algorithm
Uses HMAC-SHA256 to sign subscription parameters.

Signature Steps:

For each parameter object in the args array, sort by key name alphabetically, then concatenate key-value pairs directly (no separator)
Example: {"symbol": "btc_usdt"} -> "symbolbtc_usdt"
Place all concatenated strings into an array: ["symbolbtc_usdt"]
Convert the array to a JSON string: ["symbolbtc_usdt"]
Use SecretKey to compute HMAC-SHA256 on the JSON string, result is a hexadecimal string
Python Example:

import hmac, hashlib, json

def generate_signature(args, secret_key):
    ordered_strings = []
    for arg in args:
        s = ""
        for k, v in sorted(arg.items()):
            s += f"{k}{v}"
        ordered_strings.append(s)

    sign_text = json.dumps(ordered_strings, separators=(',', ':'))
    return hmac.new(
        secret_key.encode('utf-8'),
        sign_text.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
Copy to clipboardErrorCopied
6.4 Request Protocol Format
6.4.1 Subscribe Request
{
    "op": "SUBSCRIBE",
    "channel": "ORDERS",
    "key": "your_access_key",
    "signature": "calculated_signature",
    "args": [
        {"symbol": "btc_usdt"}
    ]
}
Copy to clipboardErrorCopied
6.4.2 Unsubscribe Request
{
    "op": "UN_SUBSCRIBE",
    "channel": "ORDERS",
    "key": "your_access_key",
    "signature": "calculated_signature",
    "args": [
        {"symbol": "btc_usdt"}
    ]
}
Copy to clipboardErrorCopied
6.4.3 Request Field Descriptions
Field	Type	Required	Description
op	String	Yes	Operation type: SUBSCRIBE / UN_SUBSCRIBE
channel	String	Yes	Channel type, see section 6.5
key	String	Yes	AccessKey
signature	String	Yes	HMAC-SHA256 signature
args	Array	Yes	Subscription parameter array
6.5 Supported Channel Types
Channel	Description	Subscription Parameters	Details
ACCOUNT	Account balance push	{"ccy": "USDT"}	Pushes account balance changes
PRICE	Price push	{"symbol": "btc_usdt"}	Pushes mark price, index price, latest trade
ORDERS	Order push	{"symbol": "btc_usdt"}	Pushes order status changes
POSITIONS	Position push	{"symbol": "btc_usdt"}	Pushes position information changes
QUIRE_LEVERAGE	Leverage configuration push	{"symbol": "btc_usdt"}	Pushes leverage configuration changes
ALLOCATION_RATIO	Funding rate push	{"symbol": "btc_usdt"}	Pushes funding rate information
All channels require authentication; anonymous subscriptions are not supported.

6.6 Response Format
6.6.1 Subscription Success Response
{
    "event": "SUBSCRIBE",
    "args": [{"symbol": "btc_usdt"}],
    "code": 200,
    "msg": "success"
}
Copy to clipboardErrorCopied
6.6.2 Unsubscription Success Response
{
    "event": "UN_SUBSCRIBE",
    "args": [{"symbol": "btc_usdt"}],
    "code": 200,
    "msg": "success"
}
Copy to clipboardErrorCopied
6.6.3 Error Response
{
    "event": "ERROR",
    "args": [{"symbol": "btc_usdt"}],
    "code": 400,
    "msg": "signature error"
}
Copy to clipboardErrorCopied
6.6.4 Response Field Descriptions
Field	Type	Description
event	String	Event type: SUBSCRIBE / UN_SUBSCRIBE / ERROR
args	Array	Request parameter echo
code	Integer	Status code: 200 success, 400 failure
msg	String	Response message
6.7 Push Data Format
Push data is transmitted via binary messages, containing UTF-8 encoded JSON strings. After receiving a binary message, the client decodes it to UTF-8 text, then parses the JSON.

ws.onmessage = function(event) {
    if (typeof event.data === 'string') {
        // Text message: subscription response or heartbeat
        if (event.data === 'ping') {
            ws.send('pong');
            return;
        }
        const data = JSON.parse(event.data);
    } else {
        // Binary message: business data push
        const text = new TextDecoder().decode(event.data);
        const data = JSON.parse(text);
    }
};
Copy to clipboardErrorCopied
6.7.1 Account Balance Push (ACCOUNT)
{
    "arg": {
        "channel": "ACCOUNT",
        "uId": 123456
    },
    "data": [{
        "ts": 1640995200000,
        "detail": {
            "ccy": "USDT",
            "ts": 1640995200000,
            "equity": "10000.00",
            "balance": "10000.00",
            "availEq": "9000.00",
            "isolateEquity": "0.00",
            "frozenEq": "1000.00",
            "initialMargin": "500.00",
            "maintMargin": "250.00",
            "orderFrozen": "1000.00",
            "crossUpl": "100.00",
            "marginRatio": "0.00",
            "isolatedUpl": "0.00"
        }
    }]
}
Copy to clipboardErrorCopied
Field Descriptions:

Field	Type	Description
ccy	String	Currency, e.g. USDT
ts	Long	Last fund update time (millisecond timestamp)
equity	String	Total currency equity = balance + crossUpl + isolatedUpl
balance	String	Currency balance (wallet balance)
availEq	String	Available margin = balance - orderFrozen - isolatedMargin - crossedMargin
isolateEquity	String	Isolated position equity = isolatedUpl + isolatedMargin
frozenEq	String	Frozen funds = orderFrozen + isolatedMargin + crossedMargin
initialMargin	String	Initial margin (all positions combined)
maintMargin	String	Maintenance margin (all positions combined)
orderFrozen	String	Order frozen amount
crossUpl	String	Cross unrealized P&L
marginRatio	String	Margin ratio
isolatedUpl	String	Isolated unrealized P&L
6.7.2 Price Push (PRICE)
{
    "arg": {
        "channel": "PRICE",
        "symbol": "btc_usdt"
    },
    "data": [{
        "contractType": "PERPETUAL",
        "symbol": "btc_usdt",
        "idxPx": "50000.00",
        "markPx": "50005.00",
        "latestTrade": [{
            "tradeId": 123456789,
            "px": "50010.00",
            "sz": "0.1",
            "side": "BUY"
        }],
        "ts": 1640995200000
    }]
}
Copy to clipboardErrorCopied
Field Descriptions:

Field	Type	Description
contractType	String	Contract type: PERPETUAL (perpetual contract)
symbol	String	Trading pair symbol
idxPx	String	Index price
markPx	String	Mark price
latestTrade	Array	Latest trade information array
ts	Long	Data update time (millisecond timestamp)
latestTrade Fields:

Field	Type	Description
tradeId	Long	Trade ID
px	String	Trade price
sz	String	Trade quantity (contracts)
side	String	Trade side: BUY / SELL
6.7.3 Order Push (ORDERS)
{
    "arg": {
        "channel": "ORDERS",
        "uId": 123456,
        "contractType": "PERPETUAL",
        "symbol": "btc_usdt"
    },
    "orderPushType": "SINGLE",
    "data": [{
        "contractType": "PERPETUAL",
        "symbol": "btc_usdt",
        "ccy": "USDT",
        "orderId": 123456789,
        "clientOrderId": "order001",
        "px": "50000.00",
        "sz": "0.1",
        "notional": "5000.00",
        "fillNotional": "2500.00",
        "orderType": "LIMIT",
        "orderSide": "BUY",
        "positionSide": "LONG",
        "positionType": "CROSSED",
        "tgtCcy": "0.00",
        "fillMarkPx": "50005.00",
        "state": "NEW",
        "lever": 10,
        "sourceType": "DEFAULT",
        "fillPx": "50010.00",
        "tradeId": 987654321,
        "fillSz": "0.05",
        "fillPnl": "0.50",
        "fillTime": 1640995200000,
        "fillFee": "0.25",
        "fillFeeCcy": "0.000005",
        "isMaker": false,
        "accFillSz": "0.05",
        "avgPx": "50010.00",
        "fee": "0.25",
        "feeCcy": "0.000005",
        "pnl": "0.50",
        "lastPx": "50010.00",
        "algoClOrdId": null,
        "isTpLimit": false,
        "uTime": 1640995200000,
        "cTime": 1640995100000
    }]
}
Copy to clipboardErrorCopied
Field Descriptions:

Field	Type	Description
contractType	String	Contract type: PERPETUAL (perpetual contract)
symbol	String	Trading pair symbol
ccy	String	Margin currency
orderId	Long	System order ID
clientOrderId	String	Client custom order ID
px	String	Order price
sz	String	Original order quantity (contracts)
notional	String	Estimated notional value
fillNotional	String	Filled value
orderType	String	Order type: LIMIT / MARKET
orderSide	String	Order side: BUY / SELL
positionSide	String	Position side: LONG / SHORT
positionType	String	Position type: CROSSED (cross margin) / ISOLATED (isolated margin)
tgtCcy	String	Market order quantity unit
fillMarkPx	String	Mark price at fill time
state	String	Order status (see below)
lever	Integer	Leverage
sourceType	String	Order source: DEFAULT (normal) / ENTRUST (trigger order) / PROFIT (take-profit/stop-loss) / REVERSE (reverse order)
fillPx	String	Latest fill price
tradeId	Long	Latest trade ID
fillSz	String	Latest fill quantity (contracts)
fillPnl	String	Fill P&L (close position order)
fillTime	Long	Fill time (millisecond timestamp)
fillFee	String	Latest fill fee amount
fillFeeCcy	String	Latest fill fee (in coin quantity)
isMaker	Boolean	Whether Maker
accFillSz	String	Accumulated fill quantity (contracts)
avgPx	String	Average fill price
fee	String	Order accumulated fee amount
feeCcy	String	Order accumulated fee (in coin quantity)
pnl	String	P&L (close position order)
lastPx	String	Latest trade price
algoClOrdId	Long	Triggered take-profit/stop-loss ID
isTpLimit	Boolean	Whether limit take-profit
uTime	Long	Order update time (millisecond timestamp)
cTime	Long	Order creation time (millisecond timestamp)
orderPushType Description:

Value	Description
SINGLE	Single order update push
ALL	Full order snapshot push (on first subscription)
Order Status Flow:

NEW -> PARTIALLY_FILLED -> FILLED (fully filled)
NEW -> CANCELED (user canceled)
NEW -> REJECTED (order rejected)
NEW -> EXPIRED (order expired)
Copy to clipboardErrorCopied
6.7.4 Position Push (POSITIONS)
{
    "arg": {
        "channel": "POSITIONS",
        "symbol": "btc_usdt",
        "uId": 123456
    },
    "data": [{
        "positionType": "CROSSED",
        "positionModel": "LONG_SHORT",
        "positionId": 123456789,
        "positionSide": "LONG",
        "pos": "0.1",
        "availPos": "0.08",
        "upl": "50.00",
        "uplRatio": "0.1000",
        "lever": 10,
        "liqPx": "45000.00",
        "markPx": "50005.00",
        "imr": "0.00",
        "margin": "500.00",
        "mgnRatio": "0.2500",
        "mmr": "250.00",
        "adl": "0",
        "ccy": "USDT",
        "realizedPnl": "25.50",
        "cTime": 1640995000000,
        "uTime": 1640995200000,
        "pTime": 1640995201000
    }]
}
Copy to clipboardErrorCopied
Field Descriptions:

Field	Type	Description
positionType	String	Margin mode: CROSSED (cross margin) / ISOLATED (isolated margin)
positionModel	String	Position mode: LONG_SHORT (hedge mode) / AGGREGATION (one-way mode)
positionId	Long	Position ID
positionSide	String	Position side: LONG / SHORT
pos	String	Position size (contracts)
availPos	String	Available position = pos - close order pending quantity
upl	String	Unrealized P&L (based on mark price)
uplRatio	String	Unrealized P&L ratio
lever	Integer	Leverage
liqPx	String	Estimated liquidation price (-- means no liquidation risk)
markPx	String	Latest mark price
imr	String	Initial margin (shown in cross margin mode)
margin	String	Margin (shown in isolated margin mode)
mgnRatio	String	Margin ratio
mmr	String	Maintenance margin
adl	String	ADL queue indicator (0-4)
ccy	String	Margin currency
realizedPnl	String	Realized P&L
cTime	Long	Position creation time (millisecond timestamp)
uTime	Long	Position update time (millisecond timestamp)
pTime	Long	Position push time (millisecond timestamp)
6.7.5 Leverage Configuration Push (QUIRE_LEVERAGE)
{
    "arg": {
        "channel": "QUIRE_LEVERAGE",
        "symbol": "btc_usdt"
    },
    "data": {
        "contractType": "PERPETUAL",
        "symbol": "btc_usdt",
        "details": [{
            "positionType": "CROSSED",
            "positionSide": "LONG",
            "lever": 10
        }],
        "ts": 1640995200000
    }
}
Copy to clipboardErrorCopied
Field Descriptions:

Field	Type	Description
contractType	String	Contract type: PERPETUAL
symbol	String	Trading pair symbol
details	Array	Leverage configuration details array
ts	Long	Configuration update time (millisecond timestamp)
details Fields:

Field	Type	Description
positionType	String	Margin mode: CROSSED / ISOLATED
positionSide	String	Position side: LONG / SHORT
lever	Integer	Leverage
6.7.6 Funding Rate Push (ALLOCATION_RATIO)
{
    "arg": {
        "channel": "ALLOCATION_RATIO",
        "symbol": "btc_usdt"
    },
    "data": {
        "symbol": "btc_usdt",
        "allowRate": "0.0001",
        "ts": 1640995200000
    }
}
Copy to clipboardErrorCopied
Field Descriptions:

Field	Type	Description
symbol	String	Trading pair symbol
alloRate	String	Funding rate (positive: longs pay shorts; negative: shorts pay longs)
ts	Long	Rate update time (millisecond timestamp)
6.8 Heartbeat Mechanism
Server sends ping text message every 15 seconds
Client must reply with pong upon receiving ping
If no pong is received within 60 seconds, server actively disconnects
It is recommended that clients implement automatic reconnection and re-subscription logic
6.9 Error Handling
6.9.1 Common Errors
Error Code	Error Message	Description
400	signature error	Signature verification failed
400	no market account	Account does not exist or futures trading is not enabled
400	Invalid parameter	Request parameter format error
6.9.2 Other Exceptions
key field is empty: Connection is silently closed
API has been deleted or disabled: Signature verification fails
Futures trading permission not enabled: Signature verification fails
JSON parsing error: Connection is closed
6.10 Data Transmission Notes
6.10.1 Message Types
Direction	Format	Description
Client -> Server	JSON text	Subscribe/unsubscribe requests
Server -> Client (response)	JSON text	Subscription confirmation, error responses
Server -> Client (push)	Binary (UTF-8 JSON)	Business data push
Server -> Client (heartbeat)	Text ping	Heartbeat detection
Client -> Server (heartbeat)	Text pong	Heartbeat response
6.10.2 Numeric Precision
All price and quantity fields are string types to avoid floating-point precision loss
It is recommended to use high-precision numeric types such as BigDecimal for processing
6.10.3 Timestamps
All timestamps are millisecond-level Unix timestamps
6.11 Important Notes
SecretKey must be stored securely and must not be leaked
Properly handle connection disconnection and reconnection logic
Respond to server heartbeats promptly to avoid connection disconnection
Correctly distinguish between text messages and binary messages
Avoid overly frequent subscribe/unsubscribe operations
A single connection can subscribe to multiple channels and multiple trading pairs simultaneously
On first subscription to the ORDERS channel, the server will push a full order snapshot (orderPushType: "ALL")
7. Error Codes
7.1 Notes
Any response with code != 0 is an error; the msg field carries the human-readable message for that error code.
Auth-layer error codes (signature/timestamp/nonce checks) are returned directly by the gateway filter, and msg is the raw error code string shown below.
Business-layer error codes (BusinessException) are translated into a localized message by the server's global exception handler; if no translation is configured for a code, msg falls back to the raw error code string. Always branch on the error code itself, not on the msg text.
Parameter validation failures (e.g. @NotBlank/@Min annotations on request DTOs) are collapsed into invalid_method (JSON body validation failure) or invalid_param (query parameter validation failure) — field-level error codes are never returned for these cases.
7.2 Authentication & Signature
Error Code	Trigger Condition
sign-error	Missing X-API-KEY/X-Signature/X-Nonce header, or the path did not match the public allow-list
timestamp-error	Missing X-Timestamp, or the client timestamp deviates from server time by more than 30 seconds
nonce-reused	The same X-Nonce was reused within its validity window (replay protection)
not-find-user-api	The accessKey does not exist, or the API Key has been deleted
user-api-is-past-due	The API Key has expired
user-api-is-forbidden	The API Key has been disabled
contract-not-support	The account does not have contract trading permission
open-auth-version-err	The API Key is not a V2 API Key
not-open-contract	Account info not found, or the contract account is not opened
not-at-white-list	The request source IP is not in the accessKey's allowed IP list
code-sign-not-match	Signature mismatch (computed signature does not match the provided one)
7.3 Generic Parameter Validation
Error Code	Trigger Condition
invalid_method	JSON request body validation failed, e.g. a required field is missing
invalid_param	Query parameter validation failed or type mismatch
invalid_params	Business-layer composite parameter validation failed (e.g. close quantity exceeds position size, invalid parameter combination)
invalid_direction	Cursor pagination direction parameter is not NEXT/PREV
Interval_Service_Error	Uncategorized internal service exception
system-error	Internal system error
7.4 Trading Pair & Market Data
Error Code	Trigger Condition
invalid_symbol	Trading pair does not exist, or does not belong to the current API Key's contract type
invalid_coin	Coin does not exist or is not enabled
invalid_interval	Kline interval parameter is invalid
invalid_time	Time range parameter is invalid
invalid_level	Depth level parameter is invalid
invalid_num	Count parameter is invalid (e.g. number of trade records)
invalid_limit	Pagination/list count parameter exceeds the allowed range
7.5 Orders
Error Code	Trigger Condition
invalid_price	Order price is invalid (out of allowed range, precision mismatch, etc.)
invalid_quantity	Order quantity is invalid
invalid_quantity_scale	Order quantity precision does not match the trading pair's requirement
invalid_time_in_force	Time-in-force does not match the order type
invalid_trigger_profit_price	Take-profit trigger price is invalid
invalid_trigger_stop_price	Stop-loss trigger price is invalid
invalid_stop_price	Trigger order stop price is invalid
invalid_order	Order not found
invalid_state	Order's current state does not allow this operation (e.g. cancelling a completed order)
not-find-account	Account not found
Forbidden	No permission to operate on this resource
fail	Operation failed (downstream system returned failure)
quantity_can_not_less_than	Order quantity is below the allowed minimum
price_cannot_greater_than_stop_price_of	Order price cannot be higher than the corresponding stop price
price_cannot_less_than_stop_price_of	Order price cannot be lower than the corresponding stop price
trigger_profit_price_less_than_entry_price	Take-profit trigger price is below entry price (invalid for long positions)
trigger_profit_price_less_than_current_price	Take-profit trigger price is below current price (invalid for long positions)
trigger_profit_price_more_than_entry_price	Take-profit trigger price is above entry price (invalid for short positions)
trigger_profit_price_more_than_current_price	Take-profit trigger price is above current price (invalid for short positions)
trigger_stop_price_more_than_entry_price	Stop-loss trigger price is above entry price (invalid for long positions)
trigger_stop_price_more_than_current_price	Stop-loss trigger price is above current price (invalid for long positions)
trigger_stop_price_less_than_entry_price	Stop-loss trigger price is below entry price (invalid for short positions)
trigger_stop_price_less_than_current_price	Stop-loss trigger price is below current price (invalid for short positions)
7.6 Positions
Error Code	Trigger Condition
invalid_leverage	Leverage is invalid (out of the trading pair's allowed range)
invalid_margin	Add/reduce margin amount is invalid
invalid_position_side	Position side parameter is invalid, or does not match the position mode
buy_sell_model_only_aggregation	This operation is not supported in hedge mode; only one-way (AGGREGATION) mode supports it
7.7 Balance
Error Code	Trigger Condition
invalid_type	Transaction type filter parameter is invalid
7.8 Async Position History Export
Error Code	Trigger Condition
file_not_ready	The export file has not finished generating yet
file_generate_failed	Export file generation failed
request count limit	Export/download rate limit exceeded (monthly export count, hourly download count)
invalid_params	Invalid downloadId, or it does not belong to the current account
8. FAQ
8.1 How to obtain an API Key?
Please contact the OneBullEx official team:

Email: it@onebullex.com
Website: https://www.onebullex.com
8.2 How long is the signature valid?
The signature timestamp is valid for 30 seconds. Please ensure your server time is synchronized.

8.3 What are the rate limiting rules?
Rate limiting is based on API Key and IP address. Please contact customer service for specific rate limiting rules.

8.4 What is the difference between isolated margin and cross margin?
Isolated (MarginMode=1): Each position has independent margin, risk is isolated
Cross (MarginMode=2): All positions share margin, higher capital efficiency
8.5 How to handle network errors?
Recommended strategies:

Use timeout mechanism (recommended 5-10 seconds)
Implement retry mechanism (recommended 3 retries)
Log failed requests for manual processing
8.6 What are the common reasons for order placement failure?
Common reasons:

Insufficient balance
Invalid price (exceeds allowed range)
Invalid quantity (below minimum or above maximum)
Trading pair is suspended
System maintenance in progress
Please check the error code and error message for specific reasons.

8.7 How to check WebSocket connection status?
The WebSocket server periodically pushes heartbeat messages. If no heartbeat is received for an extended period, please reconnect.

9. Support
Team: OneBullEx Team
Website: https://www.onebullex.com
Email: it@onebullex.com

If you have any API integration questions, technical support, or business cooperation needs, please feel free to contact us.

Document Version: 2.1.1
Last Updated: 2026-09-22

