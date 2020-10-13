import asyncio

from app.services.sso_client import SSOClient
from app import config


async def main():
    for credentials in config.TEST_ACCOUNTS:
        tokens = await SSOClient.sso_login(**credentials)
        access = tokens.get('access')
        print(credentials, access)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
