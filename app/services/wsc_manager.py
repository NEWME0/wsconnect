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
            await self._listen_until_disconnected(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        """ Delete websocket from channel and close it for client """
        self._connections.remove(websocket)
        await websocket.close(code=1000)

    async def send(self, message: str) -> Tuple[int, int]:
        """ Send message to all websockets in channel """
        coroutines = [self._safe_send(websocket, message) for websocket in self._connections]
        results = await gather(*coroutines)
        return results.count(True), results.count(False)

    async def _safe_send(self, websocket: WebSocket, message: str):
        """ Try to send message to websocket """
        try:
            await websocket.send_text(data=message)
            return True
        except WebSocketDisconnect:
            await self.disconnect(websocket)
            return False

    async def _listen_until_disconnected(self, websocket: WebSocket):
        """ Listen socket until it is closed by client """
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

    async def connect(self, channel_id: str, websocket: WebSocket) -> None:
        """ Connect websocket to channel """
        await self._channels[channel_id].connect(websocket, keep_alive=True)
        await self._destroy_channel_if_is_empty(channel_id)

    async def disconnect(self, channel_id: str, websocket: WebSocket) -> None:
        """ Disconnect websocket from channel """
        await self._channels[channel_id].disconnect(websocket)
        await self._destroy_channel_if_is_empty(channel_id)

    async def send(self, channel_id: str, message: str) -> Tuple[int, int]:
        """ Send message to channel """
        sent, fail = await self._send_message_if_channel_exists(channel_id, message)
        return sent, fail

    async def push(self, message: str) -> Tuple[int, int]:
        """ Send message to all channels """
        coroutines = [self._send_message_if_channel_exists(channel_id, message) for channel_id in self._channels]
        results = await gather(*coroutines)
        total_sent, total_fail = map(sum, zip(*results))
        return total_sent, total_fail

    async def _destroy_channel_if_is_empty(self, channel_id):
        """ Delete channel if it is empty """
        if channel_id in self._channels:
            if self._channels[channel_id].is_empty:
                del self._channels[channel_id]

    async def _send_message_if_channel_exists(self, channel_id, message):
        if channel_id in self._channels:
            return await self._channels[channel_id].send(message)
        else:
            return 0, 0
