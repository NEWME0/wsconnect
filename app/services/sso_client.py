from app import config
from app.common.service_client_session import ServiceClientSession


class SSOClient(ServiceClientSession):
    _base_url = config.SSO_DOMAIN

    @classmethod
    async def ws_sso_auth(cls, token):
        """
            Return user data or None.
            Usage:
            user = await SSOClient.ws_sso_auth(<token>)
            if user:
                # do things with user data
        """

        path = 'authorization/token/service/verify/'
        data = {
            'service_token': config.SSO_SERVICE_TOKEN,
            'token': token
        }
        async with cls() as session:
            response = await session.post(path=path, data=data)
            if response.status == 200:
                return await response.json()
