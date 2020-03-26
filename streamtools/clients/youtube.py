from pprint import pprint

import aiohttp
import httplib2
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from streamtools.base import ChatMessage
from streamtools.utils import fetch

API_MESSAGES = "https://www.googleapis.com/youtube/v3/liveChat/messages"


async def messages():
    async with aiohttp.ClientSession() as session:
        while True:
            response = await fetch(session, API_MESSAGES)


def login():
    flow = flow_from_clientsecrets(
        "client_secrets.json",
        scope="https://www.googleapis.com/auth/youtube.readonly",
        message="Login using OAuth2",
    )
    storage = Storage("credentials-secrets.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    api = build("youtube", "v3", http=credentials.authorize(httplib2.Http()))

    response = (
        api.liveBroadcasts()
        .list(part="snippet", broadcastStatus="all", broadcastType="all",)
        .execute()
    )

    pprint(response, indent=2)


async def start(queue, config):
    await queue.put(ChatMessage(source="youtube", author="mariocesar", content="Hola",))
