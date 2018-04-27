from .base import BaseApplication
from message import SCPEnvelop, TXEnvelop
from herder import Herder


class Application(BaseApplication):
    consensus = None
    herder = None

    def __init__(self, consensus, transport=None):
        super(Application, self).__init__(consensus.localNode, transport)
        self.consensus = consensus
        if transport:
            self.consensus.set_transport(transport)
        else:
            from overlay.default_http import Transport
            self.consensus.set_transport(Transport(bind=(
                '0.0.0.0',
                consensus.localNode.endpoint.port,
            )))
        self.herder = Herder(self.consensus, transport)

    def to_dict(self):
        return dict(
            node=self.node.to_dict(),
            consensus=self.consensus.to_dict(),
        )

    def receive_tx_envelop(self, txEnvelop):
        assert isinstance(txEnvelop, TXEnvelop)
        self.herder.receiveTransaction(txEnvelop)
        return

    def receive_scp_envelop(self, scpEnvelop):
        assert isinstance(scpEnvelop, SCPEnvelop)
        self.herder.receiveSCPMessage(scpEnvelop)
        return

    def is_guarantee_liveness(self):
        return self.consensus.is_guarantee_liveness()
