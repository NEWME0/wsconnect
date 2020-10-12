from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from app.services.channels import ChannelManager


router = APIRouter(default_response_class=JSONResponse)
manager = ChannelManager()


@router.get('/channels')
async def channels_list():
    result = {}

    for channel_id, connections in manager.connections.items():
        result[channel_id] = len(connections)

    return JSONResponse(result)
