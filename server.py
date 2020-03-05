import io
import logging
from asyncio import AbstractEventLoop
from typing import Optional

import socketio
from aiohttp import web
from aiologger import Logger
from aiologger.formatters.base import Formatter
from aiologger.handlers.streams import AsyncStreamHandler
from aiologger.levels import LogLevel, check_level
from aiologger.records import LogRecord

import hello
from redirect_stdout import stdout_redirector

formatter = Formatter(
    fmt='[{name}] {asctime} {levelname}: {message}',
    datefmt='%m/%d/%Y %H:%M:%S',
    style='{'
)

logger_server = Logger(name='server', level=LogLevel.DEBUG)
logger_stdout = Logger(name="s4l", level=LogLevel.DEBUG)

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

class SocketIOLogRedirect(AsyncStreamHandler):
    async def emit(self, record: LogRecord):
        await sio.emit('log', f"[{record.name}] {record.asctime} {record.levelname}: {record.get_message()}")

logger_stdout.add_handler(SocketIOLogRedirect())
logger_server.add_handler(SocketIOLogRedirect())

class LoggerSink(io.BytesIO):
    def __init__(self, logger):
        self.logger = logger

    def write(self, buf):
        msg = buf.decode('utf-8').rstrip('\n')
        self.logger.debug(f"Message from C {msg}")

f = LoggerSink(logger_stdout)


async def background_task():
    count = 0
    while True:
        await sio.sleep(1)
        count += 1
        await logger_server.debug(f'This is log number {count} from server')

async def background_ctask():
    count = 0
    while True:
        with stdout_redirector(f):
            hello.stdout("Foo")
            hello.stderr("Bar")
        
        await sio.sleep(1.0)

@sio.event
async def on_connect(sid, environ):
    await logger_server.debug(f'connect {sid}')
    await sio.emit('my_message', "asdfasdf")

@sio.event
async def disconnect(sid):
    print(sid, type(sid))
    await logger_server.debug(f'disconnect {sid}')

if __name__ == '__main__':
    sio.start_background_task(background_task)
    sio.start_background_task(background_ctask)
    web.run_app(app)
