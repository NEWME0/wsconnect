from typing import List, Tuple
from asyncio import gather
from collections import defaultdict

from fastapi.websockets import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from app.common.singleton import SingletonMeta


class Channel:
    def __init__(self):
        self._connections: List[WebSocket] = []

    @property
    def connections(self):
        return self._connections

    async def connect(self, websocket: WebSocket, keep_alive: bool = True) -> None:
        self._connections.append(websocket)
        if keep_alive:
            await self._idle(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        self._connections.remove(websocket)
        await websocket.close(code=1000)

    async def send(self, message: str) -> Tuple[int, int]:
        tasks = [self._send(websocket, message) for websocket in self._connections]
        result = await gather(*tasks)
        return result.count(True), result.count(False)

    async def _send(self, websocket: WebSocket, data: str):
        try:
            await websocket.send_text(data=data)
            return True
        except WebSocketDisconnect:
            await self.disconnect(websocket)
            return False

    async def _idle(self, websocket: WebSocket):
        try:
            while websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.receive()
        except RuntimeError:
            await self.disconnect(websocket)


class ChannelManager(metaclass=SingletonMeta):
    def __init__(self):
        self._channels = defaultdict(Channel)

    @property
    def channels(self):
        return self._channels

    async def connect(self, channel_id: str, websocket: WebSocket) -> None:
        await self._channels[channel_id].connect(websocket, keep_alive=True)

    async def send(self, channel_id: str, message: str) -> Tuple[int, int]:
        sent, fail = await self._channels[channel_id].send(message)
        return sent, fail

    async def push(self, message: str) -> Tuple[int, int]:
        sent_total = 0
        fail_total = 0

        for channel in self._channels.values():
            sent, fail = await channel.send(message)
            sent_total += sent
            fail_total += fail

        return sent_total, fail_total
