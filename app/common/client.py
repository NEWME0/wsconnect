from abc import ABC
from urllib.parse import urljoin
from aiohttp import ClientSession


class ServiceClientSession(ClientSession, ABC):
    """
        ClientSession with predefined base_url

        Usage:
        class ExampleClientSession(ServiceClientSession):
            _base_url = 'https://example.ebs'

        async with ExampleClientSession() as session:
            response = await session.get('/home')
            response = await session.post('/login', json={'username': 'admin', 'password': 'admin'})

        async with ExampleClientSession(headers={...}, cookies={...}) as session:
            response = await session.request('patch', data={...}, headers={...})
    """

    _base_url = None

    def __init__(self, *args, **kwargs):
        """ Check that base_url has value and init ClientSession """
        assert self._base_url, ValueError('_base_url should specify _base_url')
        super(ServiceClientSession, self).__init__(*args, **kwargs)

    @property
    def base_url(self):
        """ Get base_url """
        return self._base_url

    def make_url(self, path):
        """ Join base_url and path """
        return urljoin(self._base_url, path)

    def request(self, method, path, **kwargs):
        """ Handle request """
        return super(ServiceClientSession, self).request(method, self.make_url(path), **kwargs)

    def ws_connect(self, path, **kwargs):
        """ Handle websocket connection """
        return super(ServiceClientSession, self).ws_connect(self.make_url(path), **kwargs)

    def get(self, path, **kwargs):
        """ Handle GET requests """
        return super(ServiceClientSession, self).get(self.make_url(path), **kwargs)

    def options(self, path, **kwargs):
        """ Handle OPTIONS requests """
        return super(ServiceClientSession, self).options(self.make_url(path), **kwargs)

    def head(self, path, **kwargs):
        """ Handle HEAD requests """
        return super(ServiceClientSession, self).head(self.make_url(path), **kwargs)

    def post(self, path, **kwargs):
        """ Handle POST requests """
        return super(ServiceClientSession, self).post(self.make_url(path), **kwargs)

    def put(self, path, **kwargs):
        """ Handle PUT requests """
        return super(ServiceClientSession, self).put(self.make_url(path), **kwargs)

    def patch(self, path, **kwargs):
        """ Handle PATCH requests """
        return super(ServiceClientSession, self).patch(self.make_url(path), **kwargs)

    def delete(self, path, **kwargs):
        """ Handle DELETE requests """
        return super(ServiceClientSession, self).delete(self.make_url(path), **kwargs)
