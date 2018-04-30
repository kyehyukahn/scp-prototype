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
        self.nominationProtocol(index, scp)
        self.ballotProtocol(index, scp)

    def getSlotIndex(self):
        return self.slotIndex

    def getSCP(self):
        return self.scp

    def getBallotProtocol(self):
        return self.ballotProtocol

    def getLatestCompositeCandidate(self):
        return self.nominationProtocol.getLatestCompositeCandidate()

    def processEnvelop(self, scpEnvelope):
        if scpEnvelope.statementType is SCPStatementType.SCP_ST_NOMINATE:
            nominationProtocol.processEnvelope(scpEnvelope)
        else:
            ballotProtocol.processEnvelope(scpEnvelope)

    def nominate(self, value, valueprev, timeout):
        nominationProtocol.nominate(value, valueprev, timeout)

    def stopNomination(self, slotIndex):
        nominationProtocol.stopNomination(slotIndex)

    def abandonBallot(self):
        pass

    def isFullyValidated(self):
        return self.fullyValidated

    def createEnvelope(statement):
        pass

    # ** federated agreement helper functions

    # returns true if the statement defined by voted and accepted
    # should be accepted
    def federatedAccept(self):
        pass

    # returns true if the statement defined by voted
    # is ratified
    def federatedRatify(self):
        pass
