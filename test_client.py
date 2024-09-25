# Connect to socket io server

import socketio
import time

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


@sio.event
def response(data):
    print('I received a response!', data)


# Connect
sio.connect('http://localhost:8000')
sio.wait()
