from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket
from fastapi.param_functions import Depends

from app.common.depends import sso_websocket_auth
from app.services.wsc_manager import ChannelManager


router = APIRouter()
manager = ChannelManager()


@router.get('/dashboard/')
async def channel_dashboard():
    return JSONResponse(status_code=200, content={'message': 'NOT IMPLEMENTED'})


@router.websocket('/websocket/')
async def channel_websocket(websocket: WebSocket, user_id: str = Depends(sso_websocket_auth)):
    if user_id:
        channel_id = f'chat_{user_id}'
        await websocket.accept()
        await manager.connect(channel_id, websocket)
    else:
        await websocket.close(code=1000)
