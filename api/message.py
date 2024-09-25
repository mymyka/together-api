import sio
import typing as t
import socketio.exceptions as sio_exc
import deps
import sqlalchemy.orm as orm
import sqlmodel
import models


@sio.server.on('connect')
async def connect(sid, environ):
    print('Connected', sid)


@sio.server.on('disconnect')
async def disconnect(sid):
    print('Disconnected', sid)


@sio.server.event
async def begin_chat(sid, data: t.Dict[t.Literal['user_id'], int]):
    user_id = data.get('user_id')

    if user_id is None:
        raise sio_exc.ConnectionRefusedError('user_id is required')

    session = deps.SessionFactory()
    stmt = sqlmodel.select(models.User).where(models.User.id == user_id).options(
        orm.selectinload(models.User.channels)
    )
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()

    if not user:
        raise sio_exc.ConnectionRefusedError('User not found')

    for channel in user.channels:
        await sio.server.enter_room(sid, channel.id)

    await session.close()


@sio.server.event
async def send_message(sid, data: t.Dict[t.Literal['channel_id', 'message'], t.Any]):
    channel_id = data.get('channel_id')
    message = data.get('message')

    if channel_id is None:
        raise sio_exc.ConnectionRefusedError('channel_id is required')

    if message is None:
        raise sio_exc.ConnectionRefusedError('message is required')

    session = deps.SessionFactory()
    stmt = sqlmodel.select(models.Channel).where(models.Channel.id == channel_id)
    result = await session.execute(stmt)
    channel = result.scalars().one_or_none()

    if not channel:
        raise sio_exc.ConnectionRefusedError('Channel not found')

    await sio.server.emit('get message', message, room=channel.id)
    await session.close()
