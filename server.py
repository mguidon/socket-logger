import socketio
from aiohttp import web
import logging
from aiologger import Logger, formatters, levels, handlers, records

formatter = formatters.base.Formatter(
    fmt='[{name}] {asctime} {levelname}: {message}',
    datefmt='%m/%d/%Y %H:%M:%S',
    style='{'
)

logger = Logger.with_default_handlers(name=__name__,  formatter=formatter, level=levels.LogLevel.DEBUG)

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

class SocketIOLogRedirect(handlers.streams.AsyncStreamHandler):
    async def emit(self, record: records.LogRecord):
        await sio.emit('log', f"[{record.name}] {record.asctime} {record.levelname}: {record.get_message()}")

log_redirector = SocketIOLogRedirect()
logger.add_handler(log_redirector)

async def background_task():
    count = 0
    while True:
        await sio.sleep(1)
        count += 1
        await logger.debug(f'This is log number {count} from server')

@sio.event
async def on_connect(sid, environ):
    await logger.debug('connect %i', sid)
    await sio.emit('my_message', "asdfasdf")

@sio.event
async def disconnect(sid):
    print(sid, type(sid))
    await logger.debug(f'disconnect {sid}')

if __name__ == '__main__':
   sio.start_background_task(background_task)
   web.run_app(app)

    