import asyncio
import sys
from asyncio import Queue
from pathlib import Path

from streamtools.utils import loadconfig
from streamtools.relay.clients import discordc, twitch, youtube

BASEDIR = Path(__file__).parent.parent.resolve()

config = loadconfig()


async def process_queue(queue):
    print("Processing queue")

    while True:
        message = await queue.get()
        print(message)


async def run_discord(queue):
    print("Discord starting")
    await discordc.start(queue, config)


async def run_twitch(queue):
    print("Twitch starting")
    await twitch.start(queue, config)


async def run_youtube(queue):
    print("Youtube starting")
    await youtube.start(queue, config)


async def fetch_events(queue):
    return await asyncio.gather(
        run_discord(queue),  run_twitch(queue)
    )


async def main():
    queue = Queue()
    await asyncio.gather(fetch_events(queue), process_queue(queue))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    finally:
        sys.stdout.write("Bye! \n")
        loop.close()
