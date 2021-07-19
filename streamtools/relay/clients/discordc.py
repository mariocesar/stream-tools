import discord
from streamtools.base import ChatEvent, EventType


class Client(discord.Client):
    def __init__(self, queue, config, *args, **kwargs):
        self.queue = queue
        self.config = config
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        await self.queue.put(ChatEvent(type=EventType.READY, source="discord",))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.name == self.config["sources"]["discord"]["channel"]:
            await self.queue.put(
                ChatEvent(
                    type=EventType.MESSAGE,
                    source="discord",
                    author=message.author.name,
                    content=message.content,
                )
            )


def login():
    ...


async def start(queue, config):
    client = Client(queue, config)

    try:
        await client.start(config["credentials"]["discord"]["token"])
    finally:
        await client.logout()
