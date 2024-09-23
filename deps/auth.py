import fastapi
import sqlalchemy.ext.asyncio as sa_async
import models
from .database import get_session


def get_user_id(
    x_user_id: int = fastapi.Header(...),
) -> int:
    return x_user_id


async def get_user(
    id_: int = fastapi.Depends(get_user_id),
    session: sa_async.AsyncSession = fastapi.Depends(get_session),
):
    user = await session.get(models.User, id_)
    if user is None:
        raise fastapi.HTTPException(status_code=404)
    return user
