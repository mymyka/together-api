import sqlmodel
import typing as t

from .users_channels import UserChannel


class User(sqlmodel.SQLModel, table=True):
    id: t.Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    username: str = sqlmodel.Field(max_length=100, unique=True)
    password: str

    channels: t.List["Channel"] = sqlmodel.Relationship(  # type: ignore
        link_model=UserChannel,
        back_populates="users",
        sa_relationship_kwargs={"lazy": "selectin", "uselist": True},
    )
    messages: t.List["Message"] = sqlmodel.Relationship(  # type: ignore
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin", "uselist": True},
    )
