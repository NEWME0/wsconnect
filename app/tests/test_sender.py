from urllib.parse import urljoin

import asyncio
import aiohttp


WS_CONNECT_DOMAIN = 'http://127.0.0.1:8000/'


async def test_health():
    async with aiohttp.ClientSession() as session:
        url = urljoin(WS_CONNECT_DOMAIN, 'health')
        response = await session.get(url)
        content = await response.json()
        print('test_health', response.status, content)


async def test_send_message(channel_id, message):
    async with aiohttp.ClientSession() as session:
        url = urljoin(WS_CONNECT_DOMAIN, f'channel/send/{channel_id}')
        response = await session.post(url, json=message)
        content = await response.json()
        print('test_send_message', response.status, content)


async def test_send_broadcast(message):
    async with aiohttp.ClientSession() as session:
        url = urljoin(WS_CONNECT_DOMAIN, 'channel/send')
        response = await session.post(url, json=message)
        content = await response.json()
        print('test_send_broadcast', response.status, content)


async def main():
    await test_health()

    for i in range(5):
        await test_send_message(channel_id='channel_001', message={'message': f'Channel message for "channel_001" {i}'})
        await asyncio.sleep(1)

    for i in range(5):
        await test_send_message(channel_id='channel_002', message={'message': f'Channel message for "channel_002" {i}'})
        await asyncio.sleep(1)

    for i in range(5):
        await test_send_message(channel_id='channel_003', message={'message': f'Channel message for "channel_003" {i}'})
        await asyncio.sleep(1)

    for i in range(5):
        await test_send_broadcast(message={'message': f'Broadcast message {i}'})
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
