from abc import ABC
from urllib.parse import urljoin
from aiohttp import ClientSession


class ServiceClientSession(ClientSession, ABC):
    _base_url = None

    def __init__(self, *args, **kwargs):
        if self._base_url is None:
            raise ValueError('base_url should not be None')

        super(ServiceClientSession, self).__init__(*args, **kwargs)

    def _make_url(self, path):
        return urljoin(self._base_url, path)

    def request(self, method, path, **kwargs):
        return super(ServiceClientSession, self).request(method, self._make_url(path), **kwargs)

    def get(self, path, **kwargs):
        return super(ServiceClientSession, self).get(self._make_url(path), **kwargs)

    def options(self, path, **kwargs):
        return super(ServiceClientSession, self).options(self._make_url(path), **kwargs)

    def head(self, path, **kwargs):
        return super(ServiceClientSession, self).head(self._make_url(path), **kwargs)

    def post(self, path, **kwargs):
        return super(ServiceClientSession, self).post(self._make_url(path), **kwargs)

    def put(self, path, **kwargs):
        return super(ServiceClientSession, self).put(self._make_url(path), **kwargs)

    def patch(self, path, **kwargs):
        return super(ServiceClientSession, self).patch(self._make_url(path), **kwargs)

    def delete(self, path, **kwargs):
        return super(ServiceClientSession, self).delete(self._make_url(path), **kwargs)
