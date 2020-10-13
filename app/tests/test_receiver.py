import asyncio

from app.tests.common import TestClient
from app import config


async def main():
    await asyncio.gather(
        TestClient.open_websocket(config.TEST_TOKEN),
        TestClient.open_websocket(config.TEST_TOKEN),
        TestClient.open_websocket(config.TEST_TOKEN),
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
