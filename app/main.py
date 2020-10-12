from fastapi.applications import FastAPI
from fastapi.responses import JSONResponse

from app.routers import channels
from app.routers import health
from app.routers import debug


app = FastAPI()

app.include_router(prefix='/channels', router=channels.router, default_response_class=JSONResponse)
app.include_router(prefix='/health', router=health.router, default_response_class=JSONResponse)
app.include_router(prefix='/debug', router=debug.router, default_response_class=JSONResponse)
