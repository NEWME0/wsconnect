from app import config
from app.common.service_client_session import ServiceClientSession


class SSOClient(ServiceClientSession):
    _base_url = config.SSO_DOMAIN

    @classmethod
    async def ws_sso_auth(cls, token):
        path = 'authorization/token/service/verify/'
        data = {
            'service_token': config.SSO_SERVICE_TOKEN,
            'token': token
        }
        async with cls() as session:
            response = await session.post(path=path, data=data)
            if response.status == 200:
                return await response.json()

    @classmethod
    async def sso_login(cls, username, password):
        path = 'authorization/token/'
        data = {
            'service_token': config.SSO_SERVICE_TOKEN,
            "username": username,
            "password": password
        }
        async with cls() as session:
            response = await session.post(path=path, data=data)
            if response.status == 200:
                return await response.json()
