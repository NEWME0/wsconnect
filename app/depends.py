from aiohttp.client_exceptions import *
from fastapi.requests import Request
from fastapi.websockets import WebSocket

from app.services.sso_client import SSOClientSession


__all__ = ['SSOAuth', 'SSOWebSocketAuth']


class SSOAuth:
    async def __call__(self, request: Request):
        user_token = request.headers.get('token')
        service_token = request.headers.get('service_token')
        if not user_token or not service_token:
            return None

        try:
            user_data = await SSOClientSession.sso_auth(token=user_token, service_token=service_token)
        except (ClientConnectorError,):
            return None

        if not user_data:
            return None

        return user_data


class SSOWebSocketAuth(SSOAuth):
    """
    Get user data from SSO with token and service_token.
    Should be used as Depends in Endpoint
    """
    async def __call__(self, websocket: WebSocket):
        return super(SSOWebSocketAuth, self).__call__(websocket)
