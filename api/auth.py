import fastapi
import models
import deps
import sqlalchemy.ext.asyncio as sa
import sqlalchemy.orm as orm
import sqlmodel
import schemas

router = fastapi.APIRouter()


@router.post("/login", response_model=schemas.user.UserResponse)
async def login(
    username: str,
    password: str,
    session: sa.AsyncSession = fastapi.Depends(deps.get_session),
) -> schemas.user.UserResponse:
    stmt = (
        sqlmodel.select(models.User)
        .where(models.User.username == username)
        .options(orm.selectinload("*"))
    )
    result = await session.execute(stmt)
    user: models.User = result.scalars().one_or_none()

    if user is None or user.password != password:
        raise fastapi.HTTPException(
            status_code=404, detail="Incorrect username or password"
        )

    return schemas.user.UserResponse.model_validate(user)


@router.post("/register", response_model=schemas.user.UserResponse)
async def register(
    username: str,
    password: str,
    session: sa.AsyncSession = fastapi.Depends(deps.get_session),
) -> schemas.user.UserResponse:
    stmt = (
        sqlmodel.select(models.User)
        .where(models.User.username == username)
        .options(orm.selectinload("*"))
    )
    result = await session.execute(stmt)
    user: models.User = result.scalars().one_or_none()

    if user is not None:
        raise fastapi.HTTPException(status_code=400, detail="Username already exists")

    user = models.User(username=username, password=password, channels=[])

    session.add(user)
    await session.flush()

    return schemas.user.UserResponse.model_validate(user)


@router.get("/me", response_model=schemas.user.UserResponse)
async def me(
    user: models.User = fastapi.Depends(deps.get_user),
) -> schemas.user.UserResponse:
    return schemas.user.UserResponse.model_validate(user)
