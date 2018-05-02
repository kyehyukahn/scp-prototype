from scp import SCP
from util import LoggingMixin


class NominationProtocol(LoggingMixin):
    slot = None

    roundNumber = 0

    votes = list()
    accepted = list()
    candidates = list()
    lastNominations = dict()    # <node, envelop>

    lastEnvelope = None
    roundLeaders = list()
    nominationStarted = False
    latestCompositeCandidate = None
    previousValue = None

    valueNominated = list()

    def __init__(self, index, scp):
        self.slot = scp.getSlot(index)
        roundNumber = 0

    def getLatestCompositeCandidate(self):
        return self.latestCompositeCandidate

    def processEnvelope(self, scpEnvelope):
        pass

    def nominate(self, value, valueprev, timeout):
        pass

    def stopNomination(self, slotIndex):
        pass

    def setTimer(self, timeout):
        pass
