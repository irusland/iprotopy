from typing import Optional, List

import grpc
from grpc.aio import ChannelArgumentType, ClientInterceptor

from usage.channels import create_channel
from usage.metadata import get_metadata
from usage.package.tinkoff.invest.grpc.instruments import InstrumentsService
from usage.package.tinkoff.invest.grpc.marketdata import (
    MarketDataService,
    MarketDataStreamService,
)
from usage.package.tinkoff.invest.grpc.operations import (
    OperationsService,
    OperationsStreamService,
)
from usage.package.tinkoff.invest.grpc.orders import OrdersStreamService, OrdersService
from usage.package.tinkoff.invest.grpc.sandbox import SandboxService
from usage.package.tinkoff.invest.grpc.stoporders import StopOrdersService
from usage.package.tinkoff.invest.grpc.users import UsersService


class Services:
    def __init__(
        self,
        channel: grpc.Channel,
        token: str,
        sandbox_token: Optional[str] = None,
        app_name: Optional[str] = None,
    ) -> None:
        metadata = get_metadata(token, app_name)
        sandbox_metadata = get_metadata(sandbox_token or token, app_name)
        self.instruments_service = InstrumentsService(channel, metadata)
        self.market_data_service = MarketDataService(channel, metadata)
        self.market_data_stream_service = MarketDataStreamService(channel, metadata)
        self.operations_service = OperationsService(channel, metadata)
        self.operations_stream_service = OperationsStreamService(channel, metadata)
        self.orders_stream_service = OrdersStreamService(channel, metadata)
        self.orders_service = OrdersService(channel, metadata)
        self.users_service = UsersService(channel, metadata)
        self.sandbox_service = SandboxService(channel, sandbox_metadata)
        self.stop_orders_service = StopOrdersService(channel, metadata)


class Client:
    """Sync client.

    ```python
    import os
    from tinkoff.invest import Client

    TOKEN = os.environ["INVEST_TOKEN"]

    def main():
        with Client(TOKEN) as client:
            print(client.users.get_accounts())

    ```
    """

    def __init__(
        self,
        token: str,
        *,
        target: Optional[str] = None,
        sandbox_token: Optional[str] = None,
        options: Optional[ChannelArgumentType] = None,
        app_name: Optional[str] = None,
        interceptors: Optional[List[ClientInterceptor]] = None,
    ):
        self._token = token
        self._sandbox_token = sandbox_token
        self._options = options
        self._app_name = app_name

        self._channel = create_channel(target=target, options=options)
        if interceptors is None:
            interceptors = []
        for interceptor in interceptors:
            self._channel = grpc.intercept_channel(self._channel, interceptor)

    def __enter__(self) -> Services:
        channel = self._channel.__enter__()
        return Services(
            channel,
            token=self._token,
            sandbox_token=self._sandbox_token,
            app_name=self._app_name,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._channel.__exit__(exc_type, exc_val, exc_tb)
        return False
