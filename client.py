import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def log(data):
    print("Log received")
    print(data)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:8080')
sio.wait()