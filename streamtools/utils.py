import sys
from pathlib import Path

import yaml

BASEDIR = Path(__file__).parent.parent.resolve()


def loadconfig():
    configfile = BASEDIR / "config.yml"

    if not configfile.exists():
        sys.stderr.write("Missing config file. Please create one.\n")
        sys.exit(1)

    return yaml.safe_load(configfile.open())


async def fetch(session, url, **kwargs):
    async with session.get(url, **kwargs) as response:
        if response.status > 400:
            print(response.status, url)
            print(await response.text())
            raise Exception()

        return await response.json()
