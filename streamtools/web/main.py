import asyncio
from asyncio import Queue

from aiohttp import web
from streamtools.relay.main import fetch_events

routes = web.RouteTableDef()


@routes.get("/ws/")
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    task = asyncio.create_task(fetch_events(request.app.queue))

    try:
        while True:
            message = await request.app.queue.get()
            print(message)
            await ws.send_json(message.asdata())
    finally:
        await ws.close()
        task.cancel()

    return ws


@routes.get("/")
async def landing(request):
    return web.Response(text="Hello!")


def get_application():
    app = web.Application()
    app.queue = Queue()
    app.queue.empty()
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(get_application(), port=3000)
