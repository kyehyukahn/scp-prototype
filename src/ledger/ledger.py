from utils import LoggingMixin


class Ledger(LoggingMixin):
    consensus = None
    herder = None
    ledger = list()

    def __init__(self, consensus, herder):
        self.consensus = consensus
        self.herder = herder
        self.ledger.append([0, 0])

    def externalize(self, slotIndex, value):
        self.ledger.append([slotIndex, value])

    def last(self):
        return self.legder[len(self.ledger)-1]

    def legerClosed(self, application):
        print("legder closed")
        if application is not None:
            func = getattr(application, "triggerNextLedger")
            func()
