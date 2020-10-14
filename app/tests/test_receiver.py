import asyncio

from app import config
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


async def get_access_token(username: str, password: str):
    tokens = await SSOClientSession.sso_login(
        username=username,
        password=password,
        service_token=config.SSO_SERVICE_TOKEN
    )

    if tokens:
        return tokens.get('access')


async def main():
    websocket_tasks = []

    # Test users
    for credentials in TEST_ACCOUNTS:
        access_token = await get_access_token(**credentials)
        channel_websocket = TestClient.channel_websocket(access_token, config.SSO_SERVICE_TOKEN)
        websocket_tasks.append(channel_websocket)

    # Fake users
    websocket_tasks.append(TestClient.channel_websocket('fake-token', config.SSO_SERVICE_TOKEN))

    # Connect websockets
    await asyncio.gather(*websocket_tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('\nWebsockets disconnected')
