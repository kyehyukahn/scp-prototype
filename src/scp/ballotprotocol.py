from utils import LoggingMixin


class BallotProtocol(LoggingMixin):
    consensus = None
    slotIndex = 0

    def __init__(self, consensus, slotIndex):
        self.consensus = consensus
        self.slotIndex = slotIndex

    def processEnvelope(self, scpEnvelope):
        pass

    def abandonBallot(self):
        pass
