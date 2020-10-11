import asyncio
import aiohttp
from urllib.parse import urljoin


WS_CONNECT_DOMAIN = 'http://127.0.0.1:8000'


async def test_ping():
    async with aiohttp.ClientSession() as session:
        url = urljoin(WS_CONNECT_DOMAIN, 'ping')
        response = await session.get(url)
        content = await response.json()
        assert content.get('pong') is True


async def test_send():
    async with aiohttp.ClientSession() as session:
        url = urljoin(WS_CONNECT_DOMAIN, 'send')
        data = {'message': 'Hello'}
        response = await session.post(url, data=data)
        content = await response.json()
        assert content.get('sent') is True


async def test_ws():
    async with aiohttp.ClientSession() as session:
        url = urljoin(WS_CONNECT_DOMAIN, 'ws')

        async with session.ws_connect(url) as ws:
            while True:
                response = await ws.receive()
                print(response)


async def test_main():
    await test_ping()
    await test_ws()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_main())
