import fastapi
import schemas
import deps
import sqlalchemy.ext.asyncio as sa
import sqlmodel
import models
import typing as t
import sqlalchemy.orm as so

router = fastapi.APIRouter()


@router.get(
    "/",
    response_model=t.List[schemas.channel.Channel],
)
async def get_channels(
        session: sa.AsyncSession = fastapi.Depends(deps.get_session),
) -> t.List[schemas.channel.Channel]:
    stmt = sqlmodel.select(models.Channel).options(
        so.selectinload(models.Channel.messages).selectinload(models.Message.user),
    )
    result = await session.execute(stmt)
    channels = result.scalars().all()
    return [schemas.channel.Channel.model_validate(channel) for channel in channels]


@router.post(
    "/",
    response_model=schemas.channel.Channel,
)
async def create_channel(
        name: str,
        session: sa.AsyncSession = fastapi.Depends(deps.get_session),
) -> schemas.channel.Channel:
    channel = models.Channel(
        name=name,
        messages=[],
    )
    session.add(channel)
    await session.flush()
    return schemas.channel.Channel.model_validate(channel)


@router.post(
    "/join",
    response_model=schemas.channel.Channel,
)
async def join_channel(
        channel: models.Channel = fastapi.Depends(deps.get_resource(models.Channel)),
        user: models.User = fastapi.Depends(deps.get_user),
        session: sa.AsyncSession = fastapi.Depends(deps.get_session),
) -> schemas.res.Ok:
    channel.users.append(user)
    await session.flush()
    return schemas.res.Ok()
