import asyncio
import json
from functools import lru_cache
from pathlib import Path
from pprint import pprint

import aiohttp
import httplib2
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from streamtools.base import ChatEvent, EventType
from streamtools.utils import fetch

API_MESSAGES = "https://www.googleapis.com/youtube/v3/liveChat/messages"


@lru_cache()
def get_access_token():
    return json.loads(Path("youtube-accesstoken.json").read_text())["access_token"]


async def start(queue, config):
    async with aiohttp.ClientSession() as session:
        data = await fetch(
            session,
            "https://www.googleapis.com/youtube/v3/liveBroadcasts",
            params={
                "part": "snippet",
                "broadcastStatus": "active",
                "key": config["credentials"]["youtube"]["api_key"],
            },
            headers={
                f"Authorization": f"Bearer {get_access_token()}",
                "Accept": "application/json",
            },
        )
        live_chatid = data["items"][0]["snippet"]["liveChatId"]

        async def live_chat_messages(token=None):
            return await fetch(
                session,
                "https://www.googleapis.com/youtube/v3/liveChat/messages",
                params={
                    "liveChatId": live_chatid,
                    "part": "snippet,authorDetails,id",
                    "key": config["credentials"]["youtube"]["api_key"],
                    "pageToken": token or "",
                },
                headers={
                    f"Authorization": f"Bearer {get_access_token()}",
                    "Accept": "application/json",
                },
            )

        await queue.put(ChatEvent(type=EventType.READY, source="youtube",))

        page = None

        while True:
            data = await live_chat_messages(token=page)
            page = data["nextPageToken"]

            for message in data["items"]:
                if message["kind"] == "youtube#liveChatMessage":
                    await queue.put(
                        ChatEvent(
                            type=EventType.MESSAGE,
                            source="youtube",
                            author=message["authorDetails"]["displayName"],
                            content=message["snippet"]["displayMessage"],
                        )
                    )

            await asyncio.sleep(data["pollingIntervalMillis"] / 1000)


def shell():
    storage = Storage("youtube-accesstoken.json")
    credentials = storage.get()
    api = build("youtube", "v3", credentials=credentials)

    # Getting the chat id of the latest active broadcast
    data = (
        api.liveBroadcasts().list(part="id,snippet", broadcastStatus="active").execute()
    )

    from IPython import embed

    embed()


def login():
    flow = flow_from_clientsecrets(
        "youtube-secrets.json",
        scope="https://www.googleapis.com/auth/youtube.readonly",
        message="Login using OAuth2",
    )

    storage = Storage("youtube-accesstoken.json")
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


if __name__ == "__main__":
    login()
