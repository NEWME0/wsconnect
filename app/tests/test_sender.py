import asyncio

from app.tests.common import TestClient


async def main():
    health = await TestClient.health()
    print(health)

    count = 3
    delay = 0.5

    channel_01 = 'chat_5f58e44af6d0d54fb92f9da0'
    channel_02 = 'chat_5f58e44af6d0d54fb92f9da0'
    channel_03 = 'chat_5f58e44af6d0d54fb92f9da0'

    for i in range(count):
        sent_report = await TestClient.send_message(channel=channel_01, message=f'Send message {i}')
        print(sent_report)
        await asyncio.sleep(delay)

    for i in range(count):
        sent_report = await TestClient.send_message(channel=channel_02, message=f'Send message {i}')
        print(sent_report)
        await asyncio.sleep(delay)

    for i in range(count):
        sent_report = await TestClient.send_message(channel=channel_03, message=f'Send message {i}')
        print(sent_report)
        await asyncio.sleep(delay)

    for i in range(count):
        sent_report = await TestClient.push_message(message=f'Push message {i}')
        print(sent_report)
        await asyncio.sleep(delay)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
