from scp import Node
from utils import LoggingMixin
from overlay import BaseTransport


class BaseApplication(LoggingMixin):
    node = None
    transport = None

    def __init__(self, node, transport):
        assert isinstance(node, Node)
        assert isinstance(transport, BaseTransport)

        super(BaseApplication, self).__init__()

        self.node = node
        self.transport = transport

        self.set_logging('application', node=self.node.name)

    def __repr__(self):
        return '<Consensus: %s(%s)>' % (self.node.name, self.endpoint)

    @property
    def node_name(self):
        return self.node.name

    @property
    def endpoint(self):
        return self.node.endpoint

    def to_dict(self):
        return dict(
            node=self.node.to_dict()
        )
