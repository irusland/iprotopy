class MarketDataRequest:


class MarketDataServerSideStreamRequest:
    subscribe_candles_request: SubscribeCandlesRequest
    subscribe_order_book_request: SubscribeOrderBookRequest
    subscribe_trades_request: SubscribeTradesRequest
    subscribe_info_request: SubscribeInfoRequest
    subscribe_last_price_request: SubscribeLastPriceRequest


class MarketDataResponse:


class SubscribeCandlesRequest:
    subscription_action: SubscriptionAction
    instruments: CandleInstrument
    waiting_close: bool


class CandleInstrument:
    figi: string
    interval: SubscriptionInterval
    instrument_id: string


class SubscribeCandlesResponse:
    tracking_id: string
    candles_subscriptions: CandleSubscription


class CandleSubscription:
    figi: string
    interval: SubscriptionInterval
    subscription_status: SubscriptionStatus
    instrument_uid: string
    waiting_close: bool
    stream_id: string
    subscription_id: string


class SubscribeOrderBookRequest:
    subscription_action: SubscriptionAction
    instruments: OrderBookInstrument


class OrderBookInstrument:
    figi: string
    depth: int32
    instrument_id: string
    order_book_type: OrderBookType


class SubscribeOrderBookResponse:
    tracking_id: string
    order_book_subscriptions: OrderBookSubscription


class OrderBookSubscription:
    figi: string
    depth: int32
    subscription_status: SubscriptionStatus
    instrument_uid: string
    stream_id: string
    subscription_id: string
    order_book_type: OrderBookType


class SubscribeTradesRequest:
    subscription_action: SubscriptionAction
    instruments: TradeInstrument
    trade_type: TradeSourceType


class TradeInstrument:
    figi: string
    instrument_id: string


class SubscribeTradesResponse:
    tracking_id: string
    trade_subscriptions: TradeSubscription
    trade_type: TradeSourceType


class TradeSubscription:
    figi: string
    subscription_status: SubscriptionStatus
    instrument_uid: string
    stream_id: string
    subscription_id: string


class SubscribeInfoRequest:
    subscription_action: SubscriptionAction
    instruments: InfoInstrument


class InfoInstrument:
    figi: string
    instrument_id: string


class SubscribeInfoResponse:
    tracking_id: string
    info_subscriptions: InfoSubscription


class InfoSubscription:
    figi: string
    subscription_status: SubscriptionStatus
    instrument_uid: string
    stream_id: string
    subscription_id: string


class SubscribeLastPriceRequest:
    subscription_action: SubscriptionAction
    instruments: LastPriceInstrument


class LastPriceInstrument:
    figi: string
    instrument_id: string


class SubscribeLastPriceResponse:
    tracking_id: string
    last_price_subscriptions: LastPriceSubscription


class LastPriceSubscription:
    figi: string
    subscription_status: SubscriptionStatus
    instrument_uid: string
    stream_id: string
    subscription_id: string


class Candle:
    figi: string
    interval: SubscriptionInterval
    open: Quotation
    high: Quotation
    low: Quotation
    close: Quotation
    volume: int64
    time: google.protobuf.Timestamp
    last_trade_ts: google.protobuf.Timestamp
    instrument_uid: string


class OrderBook:
    figi: string
    depth: int32
    is_consistent: bool
    bids: Order
    asks: Order
    time: google.protobuf.Timestamp
    limit_up: Quotation
    limit_down: Quotation
    instrument_uid: string
    order_book_type: OrderBookType


class Order:
    price: Quotation
    quantity: int64


class Trade:
    figi: string
    direction: TradeDirection
    price: Quotation
    quantity: int64
    time: google.protobuf.Timestamp
    instrument_uid: string
    tradeSource: TradeSourceType


class TradingStatus:
    figi: string
    trading_status: SecurityTradingStatus
    time: google.protobuf.Timestamp
    limit_order_available_flag: bool
    market_order_available_flag: bool
    instrument_uid: string


class GetCandlesRequest:
    figi: string
    from: google.protobuf.Timestamp
    to: google.protobuf.Timestamp
    interval: CandleInterval
    instrument_id: string
    candle_source_type: CandleSource


class GetCandlesResponse:
    candles: HistoricCandle


class HistoricCandle:
    open: Quotation
    high: Quotation
    low: Quotation
    close: Quotation
    volume: int64
    time: google.protobuf.Timestamp
    is_complete: bool
    candle_source: CandleSource


class GetLastPricesRequest:
    figi: string
    instrument_id: string


class GetLastPricesResponse:
    last_prices: LastPrice


class LastPrice:
    figi: string
    price: Quotation
    time: google.protobuf.Timestamp
    instrument_uid: string


class GetOrderBookRequest:
    figi: string
    depth: int32
    instrument_id: string


class GetOrderBookResponse:
    figi: string
    depth: int32
    bids: Order
    asks: Order
    last_price: Quotation
    close_price: Quotation
    limit_up: Quotation
    limit_down: Quotation
    last_price_ts: google.protobuf.Timestamp
    close_price_ts: google.protobuf.Timestamp
    orderbook_ts: google.protobuf.Timestamp
    instrument_uid: string


class GetTradingStatusRequest:
    figi: string
    instrument_id: string


class GetTradingStatusesRequest:
    instrument_id: string


class GetTradingStatusesResponse:
    trading_statuses: GetTradingStatusResponse


class GetTradingStatusResponse:
    figi: string
    trading_status: SecurityTradingStatus
    limit_order_available_flag: bool
    market_order_available_flag: bool
    api_trade_available_flag: bool
    instrument_uid: string
    bestprice_order_available_flag: bool
    only_best_price: bool


class GetLastTradesRequest:
    figi: string
    from: google.protobuf.Timestamp
    to: google.protobuf.Timestamp
    instrument_id: string


class GetLastTradesResponse:
    trades: Trade


class GetMySubscriptions:


class GetClosePricesRequest:
    instruments: InstrumentClosePriceRequest


class InstrumentClosePriceRequest:
    instrument_id: string


class GetClosePricesResponse:
    close_prices: InstrumentClosePriceResponse


class InstrumentClosePriceResponse:
    figi: string
    instrument_uid: string
    price: Quotation
    evening_session_price: Quotation
    time: google.protobuf.Timestamp


class GetTechAnalysisRequest:
    indicator_type: IndicatorType
    instrument_uid: string
    from: google.protobuf.Timestamp
    to: google.protobuf.Timestamp
    interval: IndicatorInterval
    type_of_price: TypeOfPrice
    length: int32
    deviation: Deviation
    smoothing: Smoothing


class GetTechAnalysisResponse:
    technical_indicators: TechAnalysisItem


from typing import Optional


class ClassName:
    field1: int
    field2: Optional[bool] = False
