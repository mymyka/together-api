# Connect to socket io server

import socketio
import time

sio = socketio.Client()


def get_message(data):
    print('Get Message:', data)


sio.on('get message', handler=get_message)

# Connect
sio.connect('http://localhost:8000')

sio.emit('begin_chat', {'user_id': 1})
sio.emit('send_message', {'channel_id': 1, 'message': 'Hello World!'})

sio.wait()
