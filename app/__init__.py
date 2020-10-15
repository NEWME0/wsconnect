from fastapi.responses import JSONResponse
from fastapi.applications import FastAPI

from app.routers import message, channel


app = FastAPI(
    title='Websocket channels API',
    version='0.1.1',
    description='...',
)


app.include_router(prefix='/message', router=message.router)
app.include_router(prefix='/channel', router=channel.router)


@app.get('/')
async def health():
    return JSONResponse(status_code=200, content={'health': True})
