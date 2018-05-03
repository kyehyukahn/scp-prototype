from ledger import Ledger
from message import TXEnvelop, SCPEnvelop
from overlay import BaseTransport
from utils import LoggingMixin
from scp import SCP


class Herder(LoggingMixin):
    consensus = None
    overlay = None
    ledger = None

    recievedTxs = list()
    proposedValues = list()

    pendingEnvelope = None

    slotIndex = 0
    valuePrev = ""


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
        self.legerClosed(application)

    def legerClosed(self, application):
        print("legder closed")
        if application is not None:
            func = getattr(application, "triggerNextLedger")
            func()

    def triggerNextLedger(self):
        print("triggerNextLedger()")
        self.proposedValues = self.recievedTxs
        self.valuePrev, self.slotIndex = self.ledger.latest()
        self.slotIndex += 1
        self.consensus.nominate(self.slotIndex,
                                self.proposedValues, self.valuePrev)

    def receiveTransaction(self, txEnvelop):
        assert isinstance(txEnvelop, TXEnvelop)
        # check if tx is valid
        self.recvTxs.append(txEnvelop.tx)  # no duplicates
        self.recvTxs = list(set(self.recvTxs))
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
