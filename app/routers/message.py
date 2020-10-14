from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from app.common.schemas import SendMessage, PushMessage, SentReport
from app.services.wsc_manager import ChannelManager


router = APIRouter(default_response_class=JSONResponse)
manager = ChannelManager()


@router.post('/push/', response_model=SentReport, response_class=JSONResponse)
async def push_message(schema: PushMessage):
    sent, fail = await manager.push(schema.message)
    return SentReport(sent=sent, fail=fail)


@router.post('/send/', response_model=SentReport, response_class=JSONResponse)
async def send_message(schema: SendMessage):
    sent, fail = await manager.send(schema.channel, schema.message)
    return SentReport(sent=sent, fail=fail)
