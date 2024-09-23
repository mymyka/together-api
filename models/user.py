import sqlmodel
import typing as t
import pydantic


class User(sqlmodel.SQLModel, table=True):
    id: t.Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    username: str = sqlmodel.Field(max_length=100, unique=True)
    password: str


class UserResponse(pydantic.BaseModel):
    id: int
    username: str
