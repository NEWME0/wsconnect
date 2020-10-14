from typing import Optional

from app import config
from app.common.client import ServiceClientSession


class SSOClientSession(ServiceClientSession):
    _base_url = config.SSO_DOMAIN

    @classmethod
    async def sso_auth(cls, token: str, service_token: str) -> Optional[dict]:
        """
        SSO user data with token
        :param token:
        :param service_token
        :return: {<user-data>}
        """
        path = 'authorization/token/service/verify/'
        data = {
            'service_token': service_token,
            'token': token
        }
        async with cls(raise_for_status=False) as session:
            response = await session.post(path=path, json=data)
            if response.status == 200:
                return await response.json()

    @classmethod
    async def sso_login(cls, username: str, password: str, service_token: str) -> Optional[dict]:
        """
        SSO user login
        :param username:
        :param password:
        :param service_token
        :return: {'refresh': '<refresh-token>', 'access': '<access-token>'}
        """
        path = 'authorization/token/'
        data = {
            'service_token': service_token,
            "username": username,
            "password": password
        }
        async with cls(raise_for_status=False) as session:
            response = await session.post(path=path, json=data)
            if response.status == 200:
                return await response.json()
