from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket
from pydantic import BaseModel

from app.services.channels import ChannelManager


router = APIRouter(default_response_class=JSONResponse)
manager = ChannelManager()


class Message(BaseModel):
    message: str


class Report(BaseModel):
    sent: int
    fail: int


@router.post('/send')
async def send_broadcast(message: Message):
    sent, fail = await manager.send_broadcast(message.message)
    return Report(sent=sent, fail=fail)


@router.post('/send/{channel_id}')
async def send_message(channel_id: str, message: Message):
    sent, fail = await manager.send_message(channel_id, message.message)
    return Report(sent=sent, fail=fail)


@router.websocket('/ws/{channel_id}')
async def websocket_endpoint(websocket: WebSocket, channel_id: str):
    await manager.connect(channel_id, websocket)
