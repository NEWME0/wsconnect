from typing import Optional

from app import config
from app.common.client import ServiceClientSession


class SSOClientSession(ServiceClientSession):
    _base_url: str = config.SSO_DOMAIN
    _base_session: 'SSOClientSession' = None

    @classmethod
    def base_session(cls):
        """ Get base session or create one if doesn't exist or is closed """
        if not cls._base_session or cls._base_session.closed:
            cls._base_session = cls()
        return cls._base_session

    @classmethod
    async def fetch(cls, session: 'SSOClientSession', **kwargs):
        """ Request with specific session """
        async with session.request(**kwargs) as response:
            if response.status == 200:
                return await response.json()

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
        return await cls.fetch(cls.base_session(), method='post', path=path, json=data)

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
        return await cls.fetch(cls.base_session(), method='post', path=path, json=data)
