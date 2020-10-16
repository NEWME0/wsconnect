from fastapi.responses import JSONResponse
from fastapi.applications import FastAPI

from app.routing import router
from app.services import sso_client


app = FastAPI(
    title='Websocket channels API',
    version='0.1.1',
    description='...',
)


app.include_router(prefix='', router=router)


@app.get('/')
async def health():
    return JSONResponse(status_code=200, content={'health': True})


@app.on_event('startup')
async def on_startup():
    # Initialize sso session
    await sso_client.SSOClientSession.initialize_base_session()


@app.on_event('shutdown')
async def on_shutdown():
    # Finalize sso session
    await sso_client.SSOClientSession.finalize_base_session()
