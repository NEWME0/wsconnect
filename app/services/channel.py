from typing import List, Dict, Tuple
from collections import defaultdict

from fastapi.websockets import WebSocket, WebSocketDisconnect

from app.common.singleton import SingletonMeta


class ChannelManager(metaclass=SingletonMeta):
    def __init__(self):
        self.connections: Dict[str, List[WebSocket]] = defaultdict(list)

    @classmethod
    async def _send(cls, websocket: WebSocket, message: str) -> bool:
        try:
            await websocket.send_text(data=message)
            return True
        except WebSocketDisconnect:
            return False

    @classmethod
    async def _send_many(cls, websockets: List[WebSocket], message: str) -> Tuple[int, int]:
        result = [await cls._send(websocket, message) for websocket in websockets]
        sent = result.count(True)
        fail = result.count(False)
        return sent, fail

    async def connect(self, channel_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[channel_id].append(websocket)

        # keep websocket alive
        try:
            while True:
                msg = await websocket.receive_text()
        except WebSocketDisconnect:
            await self.disconnect(channel_id, websocket)

    async def disconnect(self, channel_id: str, websocket: WebSocket) -> None:
        self.connections[channel_id].remove(websocket)
        await websocket.close()

    async def send_message(self, channel_id: str, message: str) -> Tuple[int, int]:
        websockets = self.connections[channel_id]
        sent, fail = await self._send_many(websockets, message)
        return sent, fail

    async def send_broadcast(self, message: str) -> Tuple[int, int]:
        websockets = sum(self.connections.values(), [])
        sent, fail = await self._send_many(websockets, message)
        return sent, fail
