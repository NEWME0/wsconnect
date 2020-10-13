from aiohttp import WSMsgType

from app.common.service_client_session import ServiceClientSession


class TestClient(ServiceClientSession):
    _base_url = 'http://127.0.0.1:8000/'
    _websocket_count = -1

    @classmethod
    async def health(cls):
        async with cls() as session:
            response = await session.get(path='health/')
            if response.status == 200:
                return response.status, await response.json()
            else:
                return response.status, None

    @classmethod
    async def open_websocket(cls, token):
        headers = {
            'token': token
        }

        async with cls(headers=headers) as session:
            async with session.ws_connect('channel/ws/') as websocket:
                websocket_id = cls._websocket_count = cls._websocket_count + 1
                print(f'WebSocket {websocket_id} - connected')

                while True:
                    message = await websocket.receive()

                    if message.type in (WSMsgType.TEXT, WSMsgType.BINARY):
                        print(f'WebSocket {websocket_id} - received - {message}')
                        continue

                    if message.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED, WSMsgType.ERROR):
                        print(f'WebSocket {websocket_id} - disconnected - {message}')
                        break

    @classmethod
    async def send_message(cls, channel, message):
        data = {
            'channel': channel,
            'message': message
        }

        async with cls() as session:
            response = await session.post(path='channel/send/', json=data)
            if response.status == 200:
                return response.status, await response.json()
            else:
                return response.status, None

    @classmethod
    async def push_message(cls, message):
        data = {
            'message': message,
        }

        async with cls() as session:
            response = await session.post(path='channel/push/', json=data)
            if response.status == 200:
                return response.status, await response.json()
            else:
                return response.status, None
