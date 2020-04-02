import asyncio
import sys
from asyncio import Queue
from pathlib import Path

from streamtools.clients import discordc, twitch, youtube
from streamtools.utils import loadconfig

BASEDIR = Path(__file__).parent.resolve()

queue = Queue()
config = loadconfig()


async def process_queue():
    print("Processing queue")

    while True:
        message = await queue.get()
        print(message)


async def run_discord():
    print("Discord starting")
    await discordc.start(queue, config)


async def run_twitch():
    print("Twitch starting")
    await twitch.start(queue, config)


async def run_youtube():
    print("Youtube starting")
    await youtube.start(queue, config)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(
            asyncio.gather(run_discord(), run_youtube(), run_twitch(), process_queue())
        )
    finally:
        sys.stdout.write("Bye! \n")
        loop.close()
