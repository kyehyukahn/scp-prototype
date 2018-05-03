from .nominationprotocol import NominationProtocol
from .ballotprotocol import BallotProtocol
from utils import LoggingMixin


class Slot(LoggingMixin):
    slotIndex = 0
    scp = None
    nominationProtocol = None
    ballotProtocol = None
    fullyValidated = False

    def __init__(self, index, scp):
        self.slotIndex = index
        self.scp = scp
        self.nominationProtocol = NominationProtocol(index, self)
        self.ballotProtocol = BallotProtocol(index, self)

    def getSlotIndex(self):
        return self.slotIndex

    def getSCP(self):
        return self.scp

    def getLocalNode(self):
        return self.scp.validators

    def getBallotProtocol(self):
        return self.ballotProtocol

    def getLatestCompositeCandidate(self):
        return self.nominationProtocol.getLatestCompositeCandidate()

    def processEnvelop(self, scpEnvelope):
        if scpEnvelope.statementType is SCPStatementType.SCP_ST_NOMINATE:
            self.nominationProtocol.processEnvelope(scpEnvelope)
        else:
            self.ballotProtocol.processEnvelope(scpEnvelope)

    def nominate(self, value, valueprev, timeout):
        self.nominationProtocol.nominate(value, valueprev, timeout)

    def stopNomination(self, slotIndex):
        self.nominationProtocol.stopNomination(slotIndex)

    def abandonBallot(self):
        pass

    def isFullyValidated(self):
        return self.fullyValidated

    def createEnvelope(statement):
        pass

    # ** federated agreement helper functions

    # returns true if the statement defined by voted and accepted
    # should be accepted
    def federatedAccept(self, voted, accepted, envs):
        pass

    # returns true if the statement defined by voted
    # is ratified
    def federatedRatify(self, voted, envs):
        pass
