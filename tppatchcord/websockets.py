import asyncio
import json
from typing import Any

import requests
from websockets.asyncio.client import ClientConnection
from websockets.asyncio.client import connect as ws_connect

from .api_types import Event

HELLO_OPCODE = 10
IDENTIFY_OPCODE = 2
HEARTBEAT_OPCODE = 1

DISCORD_API_VERSION = 10
DISCORD_API_BASE_URL = f"https://discord.com/api/v{DISCORD_API_VERSION}/"

DISCORD_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"

GATEWAY_URL = requests.get(DISCORD_API_BASE_URL + "gateway", headers={"User-Agent": DISCORD_USER_AGENT}).json()["url"]

INTENTS = 33280

IDENTIFY_PAYLOAD = {
    "token": None,
    "intents": INTENTS,
    "properties": {
        "$os": "windows",
        "$browser": "disco",
        "$device": "disco"
    }
}

HEARTBEAT_SKEW = 2000
WS_MAX_SIZE = 2*22

_global_context = {
    "heartbeat_interval": None,
    "sequence_number": None
}

_message_queue = asyncio.Queue()
_event_queue = asyncio.Queue()

def form_message(opcode: int, payload: Any):
    """
    Form a 'send event' message using given opcode and payload.
    https://discord.com/developers/docs/topics/gateway-events#send-events

    :param opcode: opcode
    :param payload: payload
    :returns: JSON event message
    """
    return json.dumps({"op": opcode, "d": payload})

def process_event_payload(payload: dict) -> Event:
    """
    Preprocess raw JSON data into a dataclass-like object. (api_types.py)
    Uses recordclass.dataobject type for higher performance, inheritance and low memory footprint

    :param payload: payload
    :returns: Dataclass-like Discord API stuct
    """

    #TODO(idmp152): write a switch data preprocessing
    return Event(**payload)

async def next_event() -> dict:
    """
    Get next event to process.
    Used as in XNextEvent from Xlib:
    https://tronche.com/gui/x/xlib/event-handling/manipulating-event-queue/XNextEvent.html

    :returns: raw dict processable with process_event_payload
    """
    return await _event_queue.get()

async def send_event_message(payload: dict) -> None:
    """
    Send an event message to the Gateway API
    e.g. await send_event_message({"op": 10, "d": None}) # heartbeat

    :param payload: payload
    """
    await _message_queue.put(payload)

async def init_connection(websocket: ClientConnection, token: str) -> None:
    """
    Initializes websocket connection, identifies the client and gets the heartbeat interval for later use

    :param websocket: Connected websocket to send messages to
    :param token: User (bot) identification token
    """
    IDENTIFY_PAYLOAD["token"] = token
    await websocket.send(form_message(IDENTIFY_OPCODE, IDENTIFY_PAYLOAD))
    ret = json.loads(await websocket.recv())

    if ret["op"] != HELLO_OPCODE: raise Exception("Unexpected reply")

    _global_context["heartbeat_interval"] = (ret["d"]["heartbeat_interval"] - HEARTBEAT_SKEW) / 1000


async def heartbeat(websocket: ClientConnection) -> None:
    """
    Infinite heartbeat (op 10) loop to maintain websocket connection

    :param websocket: Connected websocket
    """
    while True:
        await websocket.send(json.dumps({"op": HEARTBEAT_OPCODE, "d": _global_context["sequence_number"]}))
        await asyncio.sleep(_global_context["heartbeat_interval"])

async def read_handler(websocket: ClientConnection) -> None:
    """
    Handles incoming websocket messages for next_event() to process

    :param websocket: Connected websocket
    """
    async for message in websocket:
        await _event_queue.put(json.loads(message))

async def write_handler(websocket: ClientConnection):
    """
    Handles messages from send_event_message() and sends them to the gateway

    :param websocket: Connected websocket
    """
    while True:
        message = await _message_queue.get()
        await websocket.send(json.dumps(message))

async def main_loop(token: str) -> None:
    """
    Main loop which opens and initializes the websocket connection. Launches heartbeat, read_handler and write_handler

    :param token: User (bot) identification token
    """
    try:
        async with ws_connect(GATEWAY_URL, max_size=WS_MAX_SIZE) as websocket:
            await init_connection(websocket, token)
            await asyncio.gather(heartbeat(websocket), read_handler(websocket), write_handler(websocket))
    except asyncio.CancelledError:
        return
