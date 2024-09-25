import fastapi
import models
import deps
import sqlalchemy.ext.asyncio as sa
import sqlalchemy.orm as orm
import sqlmodel
import schemas

router = fastapi.APIRouter()


@router.post("/login", response_model=schemas.user.User)
async def login(
    username: str,
    password: str,
    session: sa.AsyncSession = fastapi.Depends(deps.get_session),
) -> schemas.user.User:
    stmt = sqlmodel.select(models.User).where(models.User.username == username)
    result = await session.execute(stmt)
    user: models.User = result.scalars().one_or_none()

    if user is None or user.password != password:
        raise fastapi.HTTPException(
            status_code=404, detail="Incorrect username or password"
        )

    return schemas.user.User.model_validate(user)


@router.post("/register", response_model=schemas.user.User)
async def register(
    username: str,
    password: str,
    session: sa.AsyncSession = fastapi.Depends(deps.get_session),
) -> schemas.user.User:
    stmt = sqlmodel.select(models.User).where(models.User.username == username)
    result = await session.execute(stmt)
    user: models.User = result.scalars().one_or_none()

    if user is not None:
        raise fastapi.HTTPException(status_code=400, detail="Username already exists")

    user = models.User(username=username, password=password, channels=[])

    session.add(user)
    await session.flush()

    return schemas.user.User.model_validate(user)


@router.get("/me", response_model=schemas.user.User)
async def me(
    user: models.User = fastapi.Depends(deps.get_user),
) -> schemas.user.User:
    return schemas.user.User.model_validate(user)
