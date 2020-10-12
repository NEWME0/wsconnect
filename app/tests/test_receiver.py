from urllib.parse import urljoin

import aiohttp
import asyncio


WS_CONNECT_DOMAIN = 'http://127.0.0.1:8000/'


async def test_websocket(channel_id):
    async with aiohttp.ClientSession() as session:
        url = urljoin(WS_CONNECT_DOMAIN, f'channels/ws/{channel_id}')

        async with session.ws_connect(url) as ws:
            print('WebSocket', url, 'connected')

            while True:
                msg = await ws.receive()

                if msg.type == aiohttp.WSMsgType.TEXT:
                    print('WebSocket', url, 'received', msg.data)

                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    print('WebSocket', url, 'closed')
                    break

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print('WebSocket', url, 'error', msg)
                    break


async def main():
    await asyncio.gather(
        test_websocket('channel_001'),
        test_websocket('channel_001'),
        test_websocket('channel_002'),
        test_websocket('channel_003'),
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
