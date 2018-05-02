from utils import LoggingMixin
from message import SCPEnvelop, TXEnvelop, SCPStatementType


class SCP(LoggingMixin):
    localNode = None
    threshold = None
    validators = None
    validators_connected = None
    transport = None
    knownSlots = dict()

    def __init__(self, node, threshold, validators, transport):
        self.localNode = node
        self.threshold = threshold
        self.validators = validators
        self.validator_connected = dict()
        self.transport = transport
        self.set_logging('SCP', node=self.localNode.name)

    def set_transport(self, transport):
        self.transport = transport

    def init(self):
        self.clear_validator_ballots()

        return

    def clear_validator_ballots(self):
        pass

    def add_to_validator_connected(self, node):
        is_new = node.name not in self.validator_connected
        if is_new:
            self.validator_connected[node.name] = node
            self.log.debug('added to validators: is_new=%s node=%s', is_new, node)
            self.log.metric(action='connected', target=node.name, validators=list(self.validator_connected.keys()))

        return

    def remove_from_validators(self, node):
        if node.name not in self.validator_connected:
            return

        del self.validator_connected[node.name]

        self.log.debug('removed from validators: %s', node)
        self.log.metric(action='removed', target=node.name, validators=list(self.validator_connected.keys()))

        return

    def all_validators_connected(self):
        return len(self.validators) + 1 == len(self.validator_connected)

    def getSlot(self, index):
        slot = self.knownSlots[index]
        if not slot:
            slot = Slot(index, self.consensus)
            self.knownSlots[index] = slot
        return slot

    def receiveEnvelop(self, scpEnvelop):
        print("receive SCPEnvelop : %s", scpEnvelop)
        return self.getSlot(scpEnvelop.slotIndex).processEnvelop(scpEnvelop)

    def nominate(self, slotIndex, value, valueprev):
        return self.getSlot(slotIndex).nominate(value, valueprev, False)

    def stopNomination(slotIndex):
        s = getSlot(slotIndex)
        if not s:
            s.stopNomination(slotIndex)

    def getLocalNode(self):
        return self.localNode

    
