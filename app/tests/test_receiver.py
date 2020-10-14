import asyncio

from app.services.sso_client import SSOClientSession
from app.tests.test_client import TestClient


TEST_ACCOUNTS = [
    {
        "username": "zone1-user@kwg-ad2.devebs.net",
        "password": "Admintest1",
    },
    {
        "username": "zone1-simple@kwg-ad2.devebs.net",
        "password": "Admintest1",
    },
    {
        "username": "zone2-user@kwg-ad2.devebs.net",
        "password": "Admintest1",
    }
]


async def main():
    websocket_tasks = []

    # Log in test users
    for credentials in TEST_ACCOUNTS:
        tokens = await SSOClientSession.sso_login(username=credentials.get('username'),
                                                  password=credentials.get('password'))
        if not tokens:
            continue

        access = tokens.get('access')
        if not access:
            continue

        websocket_tasks.append(TestClient.channel_websocket(access))

    # Log in fake user
    websocket_tasks.append(TestClient.channel_websocket('fake-token'))

    # Connect websockets
    await asyncio.gather(*websocket_tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('\nWebsockets disconnected')
