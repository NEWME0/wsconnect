from aiohttp.client_exceptions import *
from fastapi.websockets import WebSocket

from app.services.sso_client import SSOClientSession


class SSOWebSocketAuth:
    """
        Get user data from SSO with token and service_token.
        Should be used as Depends in Endpoint
    """

    async def __call__(self, websocket: WebSocket):
        user_token = websocket.headers.get('token')
        service_token = websocket.headers.get('service_token')
        if not user_token or not service_token:
            return None

        try:
            user_data = await SSOClientSession.sso_auth(token=user_token, service_token=service_token)
        except (ClientConnectorError,):
            return None

        if not user_data:
            return None

        return user_data
