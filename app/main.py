from fastapi.applications import FastAPI
from fastapi.responses import JSONResponse

from app.routers import channel
from app.routers import health
from app.routers import debug


app = FastAPI()

app.include_router(prefix='/channel', router=channel.router, default_response_class=JSONResponse)
app.include_router(prefix='/health', router=health.router, default_response_class=JSONResponse)
app.include_router(prefix='/debug', router=debug.router, default_response_class=JSONResponse)
