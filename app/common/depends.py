from typing import Optional

from fastapi.websockets import WebSocket

from app.services.sso_client import SSOClientSession


async def sso_websocket_auth(websocket: WebSocket) -> Optional[dict]:
    token = websocket.headers.get('token')
    if not token:
        return

    user = await SSOClientSession.sso_auth(token)
    if not user:
        return

    user_id = user.get('id')
    if not user_id:
        return

    return user_id
