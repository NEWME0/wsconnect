from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(default_response_class=JSONResponse)


@router.get('/', response_class=JSONResponse)
async def get_health():
    return {
        'health': True
    }
