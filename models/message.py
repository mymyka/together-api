import sqlmodel
import typing as t


class Message(sqlmodel.SQLModel, table=True):
    id: t.Optional[int] = sqlmodel.Field(primary_key=True, default=None)
    content: str = sqlmodel.Field(nullable=False)
    channel_id: int = sqlmodel.Field(
        sa_column=sqlmodel.Column(
            sqlmodel.Integer,
            sqlmodel.ForeignKey(
                "channel.id",
                ondelete="CASCADE",
            ),
            index=True,
            nullable=False,
        )
    )
    user_id: int = sqlmodel.Field(
        sa_column=sqlmodel.Column(
            sqlmodel.Integer,
            sqlmodel.ForeignKey(
                "user.id",
                ondelete="CASCADE",
            ),
            index=True,
            nullable=False,
        )
    )

    channel: "Channel" = sqlmodel.Relationship(  # type: ignore
        back_populates="messages"
    )
    user: "User" = sqlmodel.Relationship(  # type: ignore
        back_populates="messages"
    )
