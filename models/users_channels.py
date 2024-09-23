import sqlmodel


class UserChannel(sqlmodel.SQLModel, table=True):
    id: int = sqlmodel.Field(primary_key=True)
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
