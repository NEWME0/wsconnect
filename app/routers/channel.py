from typing import Optional

from pydantic import BaseModel
from starlette import status
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends

from app.services.channel import ChannelManager
from app.services.sso_client import SSOClient


class PushMessage(BaseModel):
    message: str


class SendMessage(BaseModel):
    channel: str
    message: str


class SentReport(BaseModel):
    sent: int
    fail: int


async def sso_websocket_auth(websocket: WebSocket) -> Optional[dict]:
    token = websocket.headers.get('token')
    if not token:
        return

    user = await SSOClient.ws_sso_auth(token)
    if not user:
        return

    user_id = user.get('id')
    if not user_id:
        return

    return user_id


router = APIRouter(default_response_class=JSONResponse)
manager = ChannelManager()


@router.post('/push/')
async def push_message(serializer: PushMessage):
    sent, fail = await manager.push(serializer.message)
    return SentReport(sent=sent, fail=fail)


@router.post('/send/')
async def send_message(serializer: SendMessage):
    sent, fail = await manager.send(serializer.channel, serializer.message)
    return SentReport(sent=sent, fail=fail)


@router.websocket('/ws/')
async def websocket_endpoint(websocket: WebSocket, user_id: str = Depends(sso_websocket_auth)):
    if user_id:
        channel_id = f'chat_{user_id}'
        await websocket.accept()
        await manager.connect(channel_id, websocket)
    pass