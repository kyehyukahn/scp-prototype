from .base import BaseApplication
from .event import EventManager
from message import SCPEnvelop, TXEnvelop
from herder import Herder
from ledger import Ledger


class Application(BaseApplication):
    consensus = None
    herder = None
    events = None

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
        self.events = EventManager(self)

    def start(self):
        self.herder.bootstrap(self)

    def to_dict(self):
        return dict(
            node=self.node.to_dict(),
            consensus=self.consensus.to_dict(),
        )

    def receive_tx_envelop(self, txEnvelope):
        assert isinstance(txEnvelope, TXEnvelop)
        self.events.push_element("receive_tx_envelop_event", txEnvelope)
        return

    def receive_scp_envelop(self, scpEnvelop):
        assert isinstance(scpEnvelop, SCPEnvelop)
        self.events.push_element("receive_scp_envelop_event", scpEnvelop)
        return

    def triggerNextLedger(self):
        self.events.push_element("triggerNextLedgerEvent", None)

    def is_guarantee_liveness(self):
        return self.consensus.is_guarantee_liveness()

    def receive_tx_envelop_event(self, txEnvelope):
        assert isinstance(txEnvelope, TXEnvelop)
        self.herder.receiveTransaction(txEnvelope)
        return

    def receive_scp_envelop_event(self, scpEnvelop):
        assert isinstance(scpEnvelop, SCPEnvelop)
        self.herder.receiveSCPMessage(scpEnvelop)
        return

    def triggerNextLedgerEvent(self):
        self.herder.triggerNextLedger()
