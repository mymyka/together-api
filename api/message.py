import sio
import typing as t
import socketio.exceptions as sio_exc
import deps
import sqlalchemy.orm as orm
import sqlmodel
import models


async def begin_chat(sid, user_id: int):
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


@sio.server.on('connect')
async def connect(sid, environ):
    user_id = environ.get('HTTP_X_USER_ID')
    if user_id is None:
        raise sio_exc.ConnectionRefusedError('user_id is required')
    user_id = int(user_id)

    await sio.server.save_session(sid, {'user_id': user_id})
    print(f'User {user_id} connected')

    await begin_chat(sid, user_id)


@sio.server.on('disconnect')
async def disconnect(sid):
    session = await sio.server.get_session(sid)
    print(f'User {session.get('user_id')} disconnected')


@sio.server.on('send message')
async def send_message(sid, data: t.Dict[t.Literal['channel_id', 'message'], t.Any]):
    channel_id = data.get('channel_id')
    message = data.get('message')
    user_id = (await sio.server.get_session(sid)).get('user_id')

    if channel_id is None:
        raise sio_exc.ConnectionRefusedError('channel_id is required')

    if message is None:
        raise sio_exc.ConnectionRefusedError('message is required')

    session = deps.SessionFactory()

    stmt = sqlmodel.select(models.Channel).where(models.Channel.id == channel_id)
    result = await session.execute(stmt)
    channel = result.scalars().one_or_none()

    stmt = sqlmodel.select(models.User).where(models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()

    if not channel:
        raise sio_exc.ConnectionRefusedError('Channel not found')

    if not user:
        raise sio_exc.ConnectionRefusedError('User not found')

    if channel not in user.channels:
        raise sio_exc.ConnectionRefusedError('User not in channel')

    await sio.server.emit('message', {'channel_id': channel_id, 'message': message}, room=channel_id)
