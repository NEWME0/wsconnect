from aiohttp import WSMsgType

from app.common.client import ServiceClientSession


class TestClient(ServiceClientSession):
    _base_url = 'http://127.0.0.1:8000/'
    _websocket_count = -1
    _base_session: 'TestClient' = None

    @classmethod
    def base_session(cls):
        """ Get base session or create one if doesn't exist or is closed """
        if not cls._base_session or cls._base_session.closed:
            cls._base_session = cls()
        return cls._base_session

    @classmethod
    async def fetch(cls, session: 'TestClient', **kwargs):
        """ Request with specific session """
        async with session.request(**kwargs) as response:
            if response.status == 200:
                return response.status, await response.json()
            else:
                return response.status, None

    @classmethod
    async def health(cls):
        return await cls.fetch(cls.base_session(), method='get', path='/')

    @classmethod
    async def channel_dashboard(cls):
        raise NotImplementedError()

    @classmethod
    async def channel_websocket(cls, token, service_token):
        headers = {
            'token': token,
            'service_token': service_token
        }

        async with cls(headers=headers) as session:
            try:
                async with session.ws_connect('channel/websocket/') as websocket:
                    websocket_id = cls._websocket_count = cls._websocket_count + 1
                    print(f'WebSocket {websocket_id} - connected')

                    while True:
                        message = await websocket.receive()

                        if message.type in (WSMsgType.TEXT, WSMsgType.BINARY):
                            # print(f'WebSocket {websocket_id} - received - {message}')
                            continue

                        if message.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED, WSMsgType.ERROR):
                            print(f'WebSocket {websocket_id} - disconnected - {message}')
                            break
            except Exception:
                pass
            finally:
                print('Failed to connect')

    @classmethod
    async def message_send(cls, channel, message):
        data = {
            'channel': channel,
            'message': message
        }
        return await cls.fetch(cls.base_session(), method='post', path='message/send/', json=data)

    @classmethod
    async def message_push(cls, message):
        data = {
            'message': message,
        }
        return await cls.fetch(cls.base_session(), method='post', path='message/push/', json=data)

