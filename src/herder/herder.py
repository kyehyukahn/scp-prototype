from message import TXEnvelop, SCPEnvelop
from overlay import BaseTransport
from utils import LoggingMixin
from scp import SCP

import collections as co


class Herder(LoggingMixin):
    consensus = None
    overlay = None
    pendingValues = list()

    def __init__(self, consensus, transport):
        assert isinstance(consensus, SCP)
        assert isinstance(transport, BaseTransport)
        super(Herder, self).__init__()
        self.consensus = consensus
        self.overlay = transport

    def receiveTransaction(self, txEnvelop):
        assert isinstance(txEnvelop, TXEnvelop)
        # check if tx is valid
        self.pendingValues.append(set(txEnvelop.tx))  # no duplicate
        # self.pendingValues.append(co.OrderedDict.fromkeys(txEnvelop.tx))
        return

    def receiveSCPMessage(self, scpEnvelop):
        assert isinstance(scpEnvelop, SCPEnvelop)
        self.consensus.receiveSCPMessage(scpEnvelop)
        return
