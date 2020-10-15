import asyncio

from app.tests.test_client import TestClient


async def main():
    health = await TestClient.health()
    print(health)

    count = 5
    delay = 0.2

    channel_01 = 'chat_5f61e0c8069f7e36bc6069d4'
    channel_02 = 'chat_5f61e0c8069f7e36bc6069d2'
    channel_03 = 'chat_5f61e3280a3d66896f132175'

    for i in range(count):
        sent_report = await TestClient.message_send(channel=channel_01, message=f'Send message {i}')
        print(sent_report)
        await asyncio.sleep(delay)

    for i in range(count):
        sent_report = await TestClient.message_send(channel=channel_02, message=f'Send message {i}')
        print(sent_report)
        await asyncio.sleep(delay)

    for i in range(count):
        sent_report = await TestClient.message_send(channel=channel_03, message=f'Send message {i}')
        print(sent_report)
        await asyncio.sleep(delay)

    for i in range(count):
        sent_report = await TestClient.message_push(message=f'Push message {i}')
        print(sent_report)
        await asyncio.sleep(delay)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('\nSending interrupted')
