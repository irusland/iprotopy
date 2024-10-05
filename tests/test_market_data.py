from models.marketdata import MarketDataStreamService, MarketDataRequest

service = MarketDataStreamService()
requests: list[MarketDataRequest] = [MarketDataRequest()]
for response in service.MarketDataStream(requests):
    print(response)