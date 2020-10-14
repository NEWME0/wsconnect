import asyncio

from app.services.sso_client import SSOClientSession
from app.config import TEST_TOKEN


async def main():
    user = await SSOClientSession.ws_sso_auth(TEST_TOKEN)
    if user:
        print(user.get('id'))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
