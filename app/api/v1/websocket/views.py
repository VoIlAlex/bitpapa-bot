import asyncio
import json
from logging import getLogger
from time import sleep

import redis.asyncio as redis
import async_timeout
from fastapi import WebSocket, Depends

from config import config


logger = getLogger(__name__)


async def websocket_ping(
    websocket: WebSocket
):
    await websocket.accept()
    await websocket.send_json({
        "message": "pong"
    })


async def websocket_endpoint(
    websocket: WebSocket
):
    offer_id = websocket.path_params["offer_id"]
    await websocket.accept()

    r = redis.from_url(config.REDIS_URL)
    channel = r.pubsub()
    await channel.subscribe(f"offer-channel:{offer_id}")

    while True:
        try:
            async with async_timeout.timeout(1):
                message = await channel.get_message(ignore_subscribe_messages=True)
                if not message:
                    sleep(0.1)
                    continue

                try:
                    message_data = json.loads(message["data"])
                except Exception:
                    logger.error(f"Failed to load data (not JSON): {message}")
                    continue

                if "type" not in message_data:
                    continue

                await websocket.send_json(message_data)
        except asyncio.TimeoutError:
            ...
