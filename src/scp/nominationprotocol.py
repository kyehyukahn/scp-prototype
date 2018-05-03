import hashlib
from utils import LoggingMixin, Timer


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
    valueProposed = list()

    timer = None

    def __init__(self, index, slot):
        self.slot = slot
        self.roundNumber = 0

    def getLatestCompositeCandidate(self):
        return self.latestCompositeCandidate

    def processEnvelope(self, scpEnvelope):
        pass

    def updateRoundleaders(self):
        pass

    def getNodePriority(self):
        pass

    def hashNode(self, prio, node):
        pass

    def getNodeWeight(self, qSet):
        pass

    def votedPridicate(self):
        pass

    def acceptedPridicate(self):
        pass

    def nominate(self, value, valueprev, timeout):
        _update = False

        if timeout and not self.nominationStarted:
            return False
        self.nominationStarted = True
        self.previousValue = valueprev

        self.roundNumber += 1
        print("nominate : " + str(timeout) + ", " + str(self.roundNumber))

        self.updateRoundleaders()

        timer = Timer()
        timer.setDelay(self.roundNumber + 1)
        timer.setHandler(lambda: self.slot.scp.nominateTimeout(self.slot.getSlotIndex(), value, valueprev))
        timer.start()


    def stopNomination(self, slotIndex):
        pass
