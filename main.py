import asyncio
import sys
from asyncio import Queue
from pathlib import Path

import yaml

from clients import discord, youtube

BASEDIR = Path(__file__).parent.resolve()

queue = Queue()


def loadconfig():
    configfile = BASEDIR / "config.yml"

    if not configfile.exists():
        sys.stderr.write("Missing config file. Please create one.\n")
        sys.exit(1)

    return yaml.safe_load(configfile.open())


config = loadconfig()


async def process_queue():
    print("Processing queue")

    while True:
        message = await queue.get()
        print(message)


async def run_discord():
    print("Discord starting")
    await discord.start(queue, config)


async def run_youtube():
    print("Youtube starting")
    await youtube.start(queue, config)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(
            asyncio.gather(run_discord(), run_youtube(), process_queue())
        )
    finally:
        sys.stdout.write("Bye! \n")
        loop.close()
