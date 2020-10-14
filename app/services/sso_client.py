from typing import Optional

from app import config
from app.common.client import ServiceClientSession


class SSOClientSession(ServiceClientSession):
    _base_url = config.SSO_DOMAIN

    @classmethod
    async def sso_auth(cls, token: str) -> Optional[dict]:
        """
        SSO user data with token
        :param token:
        :return: {<user-data>}
        """
        path = 'authorization/token/service/verify/'
        data = {
            'service_token': config.SSO_SERVICE_TOKEN,
            'token': token
        }
        async with cls(raise_for_status=False) as session:
            response = await session.post(path=path, json=data)
            if response.status == 200:
                return await response.json()

    @classmethod
    async def sso_login(cls, username: str, password: str) -> Optional[dict]:
        """
        SSO user login
        :param username:
        :param password:
        :return: {'refresh': '<refresh-token>', 'access': '<access-token>'}
        """
        path = 'authorization/token/'
        data = {
            'service_token': config.SSO_SERVICE_TOKEN,
            "username": username,
            "password": password
        }
        async with cls(raise_for_status=False) as session:
            response = await session.post(path=path, json=data)
            if response.status == 200:
                return await response.json()
