import urllib.parse

from utils import (
    get_module,
    LoggingMixin,
)


def get_network_module(name):
    return get_module('.' + name, package='overlay')


class BaseTransport(LoggingMixin):
    blockchain = None
    config = None

    message_received_callback = None

    def __init__(self, **config):
        super(BaseTransport, self).__init__()

        self.config = config
        self.set_requests()

    def receive(self, data):
        raise NotImplementedError()

    def write(self, data):
        raise NotImplementedError()

    def send(self, addr, message):
        raise NotImplementedError()

    def set_requests(self):
        raise NotImplementedError()

    def start(self, blockchain, message_received_callback):
        from main import BaseApplication
        assert isinstance(blockchain, BaseApplication)

        self.set_logging('transport', node=blockchain.node_name)

        self.blockchain = blockchain
        self.message_received_callback = message_received_callback

        self._start()

        return

    def _start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()


class BaseServer(LoggingMixin):
    blockchain = None
    config = None

    def __init__(self, blockchain, **config):
        super(BaseServer, self).__init__()

        self.set_logging('network', node=blockchain.node_name)

        self.blockchain = blockchain
        self.config = config

    def start(self):
        self.blockchain.transport.start(self.blockchain, self.message_received_callback)

        return

    def message_received_callback(self):
        raise NotImplementedError()

    def stop(self):
        self.blockchain.transport.stop()

        return


class Endpoint:
    scheme = None
    host = None
    port = None
    extras = None

    @classmethod
    def from_uri(cls, uri):
        parsed = urllib.parse.urlparse(uri)

        assert len(parsed.scheme) > 0
        assert len(parsed.hostname) > 0
        assert type(parsed.port) in (int,)

        return cls(
            parsed.scheme,
            parsed.hostname,
            parsed.port,
            **dict(
                map(
                    lambda x: (x[0], x[1][0]),
                    urllib.parse.parse_qs(parsed.query).items()
                )
            )
        )

    def __init__(self, scheme, host, port, **extras):
        assert type(host) in (str,)
        assert type(port) in (int,)

        self.scheme = scheme
        self.host = host
        self.port = port
        self.extras = extras

    @property
    def uri_full(self):
        return '%s%s' % (self.uri, self.get_extras())

    def get_extras(self):
        extras = ''
        if self.extras:
            extras = '?%s' % urllib.parse.urlencode(self.extras)

        return extras

    @property
    def uri(self):
        return '%(scheme)s://%(host)s:%(port)d' % self.__dict__

    def __repr__(self):
        return '<Endpoint: %s>' % self.uri_full

    def __eq__(self, b):
        assert isinstance(b, self.__class__)

        return self.host == b.host and self.port == b.port

    def update(self, **extras):
        self.extras.update(extras)

        return

    def serialize(self):
        return self.uri_full

    def get(self, k, default=None):
        return self.extras.get(k, default)

    def join(self, u):
        return urllib.parse.urljoin(self.uri, u) + self.get_extras()
