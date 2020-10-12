from typing import List, Dict, Tuple
from collections import defaultdict

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect

from pydantic import BaseModel


class ConnectionManager:
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
        while True:
            msg = await websocket.receive_text()

    async def disconnect(self, channel_id: str, websocket: WebSocket) -> None:
        self.connections[channel_id].remove(websocket)

    async def send_message(self, channel_id: str, message: str) -> Tuple[int, int]:
        websockets = self.connections[channel_id]
        sent, fail = await self._send_many(websockets, message)
        return sent, fail

    async def send_broadcast(self, message: str) -> Tuple[int, int]:
        websockets = sum(self.connections.values(), [])
        sent, fail = await self._send_many(websockets, message)
        return sent, fail


app = FastAPI()
manager = ConnectionManager()


class Message(BaseModel):
    message: str


@app.get('/health', response_class=JSONResponse)
async def get_health():
    return {
        'health': True
    }


@app.post('/send')
async def send_broadcast(message: Message):
    sent, fail = await manager.send_broadcast(message.message)

    return JSONResponse(content={
        'sent': sent,
        'fail': fail
    })


@app.post('/send/{channel_id}')
async def send_message(channel_id: str, message: Message):
    sent, fail = await manager.send_message(channel_id, message.message)

    return JSONResponse(content={
        'sent': sent,
        'fail': fail
    })


@app.websocket('/ws/{channel_id}')
async def websocket_endpoint(websocket: WebSocket, channel_id: str):
    await manager.connect(channel_id, websocket)
