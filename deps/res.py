import fastapi
import models
import typing as t
import sqlalchemy.ext.asyncio as sa
from .database import get_session
import sqlalchemy.orm as orm
import sqlmodel

_TModel = t.TypeVar("_TModel", bound=models.SQLModel)


def get_resource(
    model: t.Type[_TModel],
):
    async def _(
        id_: int = fastapi.Query(..., alias=f'{model.__name__.lower()}_id'),
        session: sa.AsyncSession = fastapi.Depends(get_session),
    ) -> _TModel:
        stmt = sqlmodel.select(model).where(model.id == id_).options(orm.selectinload('*'))
        result = await session.execute(stmt)
        resource = result.scalars().one_or_none()

        if not resource:
            raise fastapi.HTTPException(
                status_code=404, detail=f"{model.__name__} not found"
            )

        return t.cast(_TModel, resource)

    return _
