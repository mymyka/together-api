import sqlmodel
import typing as t

from .users_channels import UserChannel


class Channel(sqlmodel.SQLModel, table=True):
    id: t.Optional[int] = sqlmodel.Field(primary_key=True, default=None)
    name: str

    users: t.List["User"] = sqlmodel.Relationship(  # type: ignore
        link_model=UserChannel,
        back_populates="channels",
        sa_relationship_kwargs={
            "lazy": "lazy",
        },
    )
    messages: t.List["Message"] = sqlmodel.Relationship(  # type: ignore
        back_populates="channel",
        sa_relationship_kwargs={
            "lazy": "lazy",
        },
    )
