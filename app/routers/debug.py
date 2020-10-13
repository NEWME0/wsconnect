from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from app.services.channel import ChannelManager


router = APIRouter(default_response_class=JSONResponse)
manager = ChannelManager()


@router.get('/active_connections/')
async def channel_list():
    result = {}

    for channel_id, connections in manager.channels.items():
        result[channel_id] = len(connections)

    return JSONResponse(result)
