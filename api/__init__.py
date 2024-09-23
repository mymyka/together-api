from . import auth
import fastapi

router = fastapi.APIRouter()

router.include_router(
    auth.router,
    prefix='/auth',
    tags=['auth'],
)
