import sys
import yaml
from pathlib import Path

BASEDIR = Path(__file__).parent.parent.resolve()


def loadconfig():
    configfile = BASEDIR / "config.yml"

    if not configfile.exists():
        sys.stderr.write("Missing config file. Please create one.\n")
        sys.exit(1)

    return yaml.safe_load(configfile.open())


async def fetch(session, url, **kwargs):
    async with session.get(url, **kwargs) as response:
        return await response.json()
