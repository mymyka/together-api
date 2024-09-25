from . import auth, channels
from .message import *
import fastapi

router = fastapi.APIRouter()

router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    channels.router,
    prefix="/channels",
    tags=["channels"],
)
