from typing import List, Tuple
from asyncio import gather
from collections import defaultdict

from fastapi.websockets import WebSocket, WebSocketDisconnect

from app.common.singleton import SingletonMeta


class Channel:
    def __init__(self):
        self._connections: List[WebSocket] = []

    @property
    def connections(self):
        """ Channel connections getter """
        return self._connections

    @property
    def is_empty(self):
        """ Check if channel has at least one active websocket """
        return len(self._connections) == 0

    async def connect(self, websocket: WebSocket, keep_alive: bool = True) -> None:
        """ Add websocket to channel """
        self._connections.append(websocket)
        if keep_alive:
            await self._idle(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        """ Delete websocket from channel and close it for client """
        self._connections.remove(websocket)
        await websocket.close(code=1000)

    async def send(self, message: str) -> Tuple[int, int]:
        """ Send message to all websockets in channel """
        send_message_coroutines = [self._send(websocket, message) for websocket in self._connections]
        result = await gather(*send_message_coroutines)
        return result.count(True), result.count(False)

    async def _send(self, websocket: WebSocket, message: str):
        """ Try to send message to websocket """
        try:
            await websocket.send_text(data=message)
            return True
        except WebSocketDisconnect:
            await self.disconnect(websocket)
            return False

    async def _idle(self, websocket: WebSocket):
        """ Keep connection alive until it is closed by client """
        try:
            while True:
                await websocket.receive()
        except RuntimeError:
            await self.disconnect(websocket)


class ChannelManager(metaclass=SingletonMeta):
    def __init__(self):
        """ Init ChannelManager """
        self._channels = defaultdict(Channel)

    @property
    def channels(self):
        """ Channels getter """
        return self._channels

    async def _destroy_channel_if_empty(self, channel_id):
        """ Delete channel if it is empty """
        if channel_id in self._channels:
            if self._channels[channel_id].is_empty:
                del self._channels[channel_id]

    async def connect(self, channel_id: str, websocket: WebSocket) -> None:
        """ Connect websocket to channel """
        await self._channels[channel_id].connect(websocket, keep_alive=True)
        await self._destroy_channel_if_empty(channel_id)

    async def disconnect(self, channel_id: str, websocket: WebSocket) -> None:
        """ Disconnect websocket from channel """
        await self._channels[channel_id].disconnect(websocket)
        await self._destroy_channel_if_empty(channel_id)

    async def send(self, channel_id: str, message: str) -> Tuple[int, int]:
        """ Send message to channel """
        sent, fail = await self._channels[channel_id].send(message)
        return sent, fail

    async def push(self, message: str) -> Tuple[int, int]:
        """ Send message to all channels """
        sent_total = 0
        fail_total = 0

        for channel in self._channels.values():
            sent, fail = await channel.send(message)
            sent_total += sent
            fail_total += fail

        return sent_total, fail_total
