import typing

import sio
import socketio.exceptions as sio_exc
import deps
import sqlalchemy.orm as orm
import sqlalchemy.ext.asyncio as async_orm
import sqlmodel
import models


async def get_user(
    user_id: int,
    *,
    session: async_orm.AsyncSession,
) -> models.User:
    stmt = (
        sqlmodel.select(models.User)
        .where(models.User.id == user_id)
        .options(orm.selectinload("*"))
    )
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()

    if not user:
        raise sio_exc.ConnectionRefusedError("User not found")

    return user


async def enter_in_chats(
    sid: str,
    user: models.User,
) -> None:
    for channel in user.channels:
        await sio.server.enter_room(sid, room=channel.id)


async def exit_from_chats(
    sid: str,
    user: models.User,
) -> None:
    for channel in user.channels:
        await sio.server.leave_room(sid, room=channel.id)


@sio.server.on("connect")
async def connect(sid, environ):
    user_id = environ.get("HTTP_X_USER_ID")
    if user_id is None:
        raise sio_exc.ConnectionRefusedError("user_id is required")

    session = deps.SessionFactory()
    user = await get_user(int(user_id), session=session)
    await sio.server.save_session(sid, {"user_id": user.id})
    await enter_in_chats(sid, user)
    await session.close()


@sio.server.on("disconnect")
async def disconnect(sid):
    session = deps.SessionFactory()
    user_id = (await sio.server.get_session(sid)).get("user_id")
    user = await get_user(user_id, session=session)
    await exit_from_chats(sid, user)
    await session.close()


@sio.server.on("send message")
async def send_message(
    sid, data: typing.Dict[typing.Literal["channel_id", "message"], typing.Any]
):
    channel_id = data.get("channel_id")
    message = data.get("message")
    user_id = (await sio.server.get_session(sid)).get("user_id")

    if channel_id is None:
        raise sio_exc.ConnectionRefusedError("channel_id is required")

    if message is None:
        raise sio_exc.ConnectionRefusedError("message is required")

    session = deps.SessionFactory()

    stmt = sqlmodel.select(models.Channel).where(models.Channel.id == channel_id)
    result = await session.execute(stmt)
    channel = result.scalars().one_or_none()

    stmt = sqlmodel.select(models.User).where(models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()

    if not channel:
        raise sio_exc.ConnectionRefusedError("Channel not found")

    if not user:
        raise sio_exc.ConnectionRefusedError("User not found")

    if channel not in user.channels:
        raise sio_exc.ConnectionRefusedError("User not in channel")

    await sio.server.start_background_task(
        sio.server.emit,
        "message",
        {"channel_id": channel_id, "message": message},
        room=channel_id,
    )
