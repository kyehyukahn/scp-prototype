import copy
import hashlib
import lorem
import json

class TXEnvelop:
    signature = None
    tx = None

    def __init__(self, signature, tx):
        self.signature = signature
        self.tx = tx

    def serialize(self, to_string=False):
        o = dict(
            signature=self.signature,
            tx=self.tx,
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
            data=int(hashlib.sha256(data.encode('utf-8')).hexdigest(), 32),
        )

    @classmethod
    def from_string(cls, s):
        o = json.loads(s)

        return cls(
            o['signature'],
            o['tx'],
        )

    @classmethod
    def from_dict(cls, o):
        return cls(
            o['signature'],
            o['tx'],
        )
