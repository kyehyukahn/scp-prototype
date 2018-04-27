from utils import LoggingMixin


class Slot(LoggingMixin):
    slotIndex = 0
    nominationProtocol = None
    ballotProtocol = None
    scp = None

    def __init__(self, index, scp):
        self.slotIndex = index
        self.scp = scp
