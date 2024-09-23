import fastapi
import models
import deps
import sqlalchemy.ext.asyncio as sa
import sqlmodel

router = fastapi.APIRouter()


@router.post(
    '/login',
    response_model=models.UserResponse
)
async def login(
        username: str,
        password: str,
        session: sa.AsyncSession = fastapi.Depends(deps.get_session),
) -> models.UserResponse:
    stmt = sqlmodel.select(models.User).where(models.User.username == username)
    result = await session.execute(stmt)
    user: models.User = result.scalars().one_or_none()

    if user is None or user.password != password:
        raise fastapi.HTTPException(status_code=404, detail='Incorrect username or password')

    return models.UserResponse(id=user.id, username=user.username)


@router.post(
    '/register',
    response_model=models.UserResponse
)
async def register(
    username: str,
    password: str,
    session: sa.AsyncSession = fastapi.Depends(deps.get_session),
) -> models.UserResponse:
    stmt = sqlmodel.select(models.User).where(models.User.username == username)
    result = await session.execute(stmt)
    user: models.User = result.scalars().one_or_none()

    if user is not None:
        raise fastapi.HTTPException(status_code=400, detail='Username already exists')

    user = models.User(username=username, password=password)

    session.add(user)
    await session.flush()

    return models.UserResponse(id=user.id, username=user.username)
