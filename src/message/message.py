import enum
import hashlib


class MessageType(enum.Enum):
    ERROR = enum.auto()
    TRANSACTION = enum.auto()
    SCP_MESSAGE = enum.auto()


class SCPStatementType(enum.Enum):
    SCP_ST_PREPARE = enum.auto()
    SCP_ST_CONFIRM = enum.auto()
    SCP_ST_EXTERNALIZE = enum.auto()
    SCP_ST_NOMINATE = enum.auto()


class Ballot :
    count = 0
    value = None

    def __init__(self, count, value):
        self.count = count
        self.value = value


class SCPSTConfirm :
    quorumHash = None   # D
    ballot = None       # b
    prepare = None      # p
    preparePrime = None # p'
    nC = 0              # c.n
    nH = 0              # h.n

    def __init__(self, qh, b, p, _p, cn, hn):
        pass


class SCPSTPrepare :
    quorumHash = None   # D
    ballot = None       # b
    nPrepare = 0        # p.n
    nCommit = 0         # c.n
    nH = 0              # h.n

    def __init__(self, qh, b, pn, cn, hn):
        pass

class SCPSTExternalize:
    commitQuorumSetHash = None
    commit = None
    nH = 0

    def __init__(self, cqh, c, hn):
        pass

class SCPSTNominate:
    quorumSetHash = None    # D
    votes = list()          # X
    accepted = list()

    def __init__(self, qh, v, a):
        pass

class SCPEnvelop:
    signature = None
    nodeID = None # v
    slotIndex = None # i
    statementType = None
    envelop = None # SCPSTConfirm, SCPSTPrepare, SCPSTExternalize, SCPSTNominate

    def __init__(self, signature, nodeID, slotIndex, statementType, envelop):
        pass

class Message :
    messageType = None
    data = None

    def __init__(self, messageType, data):
        self.messageType = messageType
        self.data = data

    def __repr__(self):
        return '<Message: messageType=%(messageType)s data="%(data)s">' % self.__dict__

    def __eq__(self, a):
        return self.message_id == a.message_id and self.data == a.data

    def __gt__(self, rhs):
        return self.message_id < rhs.message_id

    def __ge__(self, rhs):
        return self < rhs or self == rhs

    def eq_id(self, rhs):
        return self.message_id == rhs.message_id

    def __copy__(self):
        return self.__class__(
            self.message_id,
            copy.copy(self.data),
        )

    def serialize(self, to_string=False):
        o = dict(
            message_id=self.message_id,
            data=self.data,
        )

        if not to_string:
            return o

        return json.dumps(o)

    @classmethod
    def new(cls, data=None):
        if data is None:
            data = '%s-%s' % (lorem.sentence().split()[0], get_uuid())

        return cls(
            get_uuid(),
            data=data,
        )

    @classmethod
    def from_string(cls, s):
        o = json.loads(s)

        return cls(
            o['message_id'],
            o['data'],
        )

    @classmethod
    def from_dict(cls, o):
        return cls(
            o['message_id'],
            o['data'],
        )
