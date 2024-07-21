import asyncio
import echo

from grpclib.client import Channel


async def main():
    channel = Channel(host="127.0.0.1", port=50051)
    service = echo.EchoStub(channel)
    response = await service.echo(echo.EchoRequest(value="hello", extra_times=1))
    print(response)

    async for response in service.echo_stream(echo.EchoRequest(value="hello", extra_times=1)):
        print(response)

    # don't forget to close the channel when done!
    channel.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
