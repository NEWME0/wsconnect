from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket
from fastapi.param_functions import Depends

from app.depends import *
from app.schemas import *
from app.services.wsc_manager import ChannelManager


router = APIRouter()
manager = ChannelManager()


@router.websocket('/channel/websocket/')
async def channel_websocket(websocket: WebSocket, user: dict = Depends(SSOWebSocketAuth())):
    if user:
        user_id = user.get('id')
        channel_id = f'chat_{user_id}'
        await websocket.accept()
        await manager.connect(channel_id, websocket)
    else:
        await websocket.close(code=1000)


@router.get('/channel/dashboard/')
async def channel_dashboard():
    content = {channel_id: len(channel.connections) for channel_id, channel in manager.channels.items()}
    return JSONResponse(status_code=200, content=content)


@router.post('/message/push/', response_model=SentReport, response_class=JSONResponse)
async def message_push(schema: PushMessage):
    sent, fail = await manager.push(schema.message)
    return SentReport(sent=sent, fail=fail)


@router.post('/message/send/', response_model=SentReport, response_class=JSONResponse)
async def message_send(schema: SendMessage):
    sent, fail = await manager.send(schema.channel, schema.message)
    return SentReport(sent=sent, fail=fail)
