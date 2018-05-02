from ledger import Ledger
from message import TXEnvelop, SCPEnvelop
from overlay import BaseTransport
from utils import LoggingMixin
from scp import SCP


class Herder(LoggingMixin):
    consensus = None
    overlay = None
    ledger = None
    pendingValues = list()

    def __init__(self, consensus, transport):
        assert isinstance(consensus, SCP)
        assert isinstance(transport, BaseTransport)
        super(Herder, self).__init__()
        self.consensus = consensus
        self.overlay = transport
        self.ledger = Ledger(self.consensus, self)

    def bootstrap(self, application):
        # sync Ledger and....
        print("bootstrap()")
        self.ledger.legerClosed(application)

    def triggerNextLedger(self):
        print("triggerNextLedger()")


    def receiveTransaction(self, txEnvelop):
        assert isinstance(txEnvelop, TXEnvelop)
        # check if tx is valid
        self.pendingValues.append(txEnvelop.tx)  # no duplicates
        self.pendingValues = list(set(self.pendingValues))
        # print("Tx Set : %s", self.pendingValues)
        return

    def receiveSCPMessage(self, scpEnvelop):
        assert isinstance(scpEnvelop, SCPEnvelop)
        self.consensus.receiveEnvelop(scpEnvelop)
        return

    def rebroadcast(self):
        pass

    def broadcast(self):
        pass
