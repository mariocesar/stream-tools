import json
import webbrowser
from pathlib import Path
from urllib.parse import urlencode

from aiohttp import client, web
from aiohttp.web_runner import GracefulExit
from streamtools.base import ChatMessage
from streamtools.utils import loadconfig
from twitchio import Message
from twitchio.ext import commands

secrets_file = Path(__file__).parent.parent.parent / "twitch_secrets.json"


class Bot(commands.Bot):
    def __init__(self, queue, config):
        data = json.loads(secrets_file.read_text())
        config = config["credentials"]["twitch"]
        self.queue = queue
        super().__init__(
            irc_token=f"oauth:{data['access_token']}",
            client_id=config["client_id"],
            nick="mariocesar_xyz",
            prefix="!",
            initial_channels=["#mariocesar_xyz"],
        )

    async def event_pubsub(self, data):
        print(f"Event {data}")

    async def event_ready(self):
        print(f"Ready | {self.nick}")

    async def event_message(self, message: Message):
        print(f"Message | {message}")

        await self.queue.put(
            ChatMessage("twitch", message.author.display_name, message.clean_content)
        )

        await self.handle_commands(message)


def login():
    config = loadconfig()
    queryparams = urlencode(
        {
            "client_id": config["credentials"]["twitch"]["client_id"],
            "redirect_uri": "http://127.0.0.1:3333/",
            "response_type": "code",
            "scope": "chat:read channel:moderate chat:edit",
        }
    )
    webbrowser.open(f"https://id.twitch.tv/oauth2/authorize?{queryparams}")

    async def handle(request):
        async with client.ClientSession() as session:
            response = await session.post(
                url=f"https://id.twitch.tv/oauth2/token",
                params={
                    "client_id": config["credentials"]["twitch"]["client_id"],
                    "client_secret": config["credentials"]["twitch"]["client_secret"],
                    "code": request.query["code"],
                    "grant_type": "authorization_code",
                    "redirect_uri": "http://127.0.0.1:3333/",
                },
            )

            content = await response.json()

            with secrets_file.open("wt") as fobj:
                fobj.write(json.dumps(content, indent=4))

            raise GracefulExit()

        return web.Response(text="received!")

    app = web.Application()
    app.add_routes([web.get("/", handle)])
    web.run_app(app, port=3333)


async def start(queue, config):
    bot = Bot(queue, config)

    await bot._ws._connect()

    try:
        await bot._ws._listen()
    except KeyboardInterrupt:
        pass
    finally:
        bot._ws.teardown()


if __name__ == "__main__":
    bot = Bot()
    bot.run()
