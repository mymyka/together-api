import fastapi
import sqlalchemy.ext.asyncio as sa_async
import models
import sqlmodel
import sqlalchemy.orm as sa_orm
from .database import get_session


def get_user_id(
    x_user_id: int = fastapi.Header(...),
) -> int:
    return x_user_id


async def get_user(
    id_: int = fastapi.Depends(get_user_id),
    session: sa_async.AsyncSession = fastapi.Depends(get_session),
):
    stmt = (
        sqlmodel.select(models.User)
        .where(models.User.id == id_)
        .options(sa_orm.selectinload('*'))
    )
    result = await session.execute(stmt)
    user: models.User = result.scalars().one_or_none()
    if user is None:
        raise fastapi.HTTPException(status_code=404)
    return user
