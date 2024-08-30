import asyncio
import requests
import json

from typing import Any, NamedTuple
from recordclass import dataobject
from websockets.asyncio.client import connect as ws_connect, ClientConnection

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

_global_context = {
    "heartbeat_interval": None,
    "sequence_number": None
}

_message_queue = asyncio.Queue()
_event_queue = asyncio.Queue()

def form_message(opcode: int, payload: Any):
    return json.dumps({"op": opcode, "d": payload})

def process_event_payload(payload: dict) -> dataobject | bool | None:
    event_type = payload["t"]

async def next_event() -> dict:
    return await _event_queue.get()

async def send_message(message: dict) -> dict:
    await _message_queue.put(message)

async def init_connection(websocket: ClientConnection, token: str) -> None:
    IDENTIFY_PAYLOAD["token"] = token
    await websocket.send(form_message(IDENTIFY_OPCODE, IDENTIFY_PAYLOAD))
    ret = json.loads(await websocket.recv())

    if ret["op"] != HELLO_OPCODE: raise Exception("Unexpected reply")

    _global_context["heartbeat_interval"] = (ret["d"]["heartbeat_interval"] - HEARTBEAT_SKEW) / 1000


async def heartbeat(websocket: ClientConnection) -> None:
    while True:
        await websocket.send(json.dumps({"op": HEARTBEAT_OPCODE, "d": _global_context["sequence_number"]}))
        await asyncio.sleep(_global_context["heartbeat_interval"])

async def read_handler(websocket: ClientConnection) -> None:
    async for message in websocket:
        payload = json.loads(message)
        event = process_event_payload(payload)
        await _event_queue.put(event)

async def write_handler(websocket: ClientConnection):
    while True:
        message = await _message_queue.get()
        await websocket.send(json.dumps(message))

async def main_loop(token: str) -> None:
    async with ws_connect(GATEWAY_URL) as websocket:
        await init_connection(websocket, token)
        await asyncio.gather(heartbeat(websocket), read_handler(websocket), write_handler(websocket))
        

asyncio.run(main_loop())