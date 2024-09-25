import socketio

sio = socketio.Client()


def get_message(data):
    print('Get Message:', data)


sio.on('message', handler=get_message)

headers = {
    'x_user_id': '1'
}

sio.connect('http://localhost:8000', headers=headers)

sio.emit('send message', {'channel_id': 1, 'message': 'Hello World'})

sio.wait()
