import os
import sqlite3
import hashlib
from datetime import datetime
from utils import LoggingMixin


class Ledger(LoggingMixin):
    consensus = None
    herder = None
    ledger = ""

    valueLatest = ""
    slotLatest = 0

    def __init__(self, consensus, herder):
        self.consensus = consensus
        self.herder = herder
        self.InitDBSqlite3()
        self.valueLatest, self.slotLatest = self.latest()

    def externalize(self, slotIndex, Tx):
        _date = datetime.now().strftime("%Y.%m.%d %H:%M")
        self.valueLatest, _ = self.latest()
        _TXs = str(Tx)
        _hashSeed = self.valueLatest + _TXs
        _valueNew = hashlib.sha256(_hashSeed.encode('utf-8')).hexdigest()
        try:
            with sqlite3.connect(self.legder) as conn:
                cur = conn.cursor()
                # Make table for Ledger
                # --------------------------------------------
                # | value | valueprev | slot | txs | datetime |
                cur.execute("""
                            INSERT INTO
                            Consensus(Value, ValuePrev, Slot, TXs,TimeWhen)
                            VALUES('%s', '%s', '%d', '%s', '%s')
                            """ % (_valueNew, self.valueLatest,
                                   slotIndex, _TXs, _date))
                conn.comit()

        except Exception as e:
            print("Error : ", e)
            if conn:
                conn.rollback()
        else:
            pass
        finally:
            if conn:
                conn.close

    def latest(self):
        try:
            with sqlite3.connect(self.legder) as conn:
                cur = conn.cursor()
                # Make table for Ledger
                # --------------------------------------------
                # | value | valueprev | slot | txs | datetime |
                cur.execute("""
                            SELECT *
                            FROM Consensus
                            WHERE TimeWhen = (SELECT MAX(TimeWhen) AS TimeWhen FROM Consensus)
                            """)
                if cur is not None:
                    row = cur.fetchone()[0]
                    if row is not None:
                        print("lastest : %s", row)
                        self.valueLatest = row[0]
                        self.slotLatest = row[2]
        except Exception as e:
            print("latest() Error : ", e)
        else:
            pass
        finally:
            if conn:
                conn.close
        return self.valueLatest, self.slotLatest

    def InitDBSqlite3(self):
        self.legder = self.consensus.localNode.name + ".db"
        # print("database name :", dbname)
        conn = None
        if os.path.exists("./" + self.legder):
            return
        try:
            with sqlite3.connect(self.legder) as conn:
                cur = conn.cursor()
                # Make table for Ledger
                # --------------------------------------------
                # | value | valueprev | slot | txs | datetime |
                cur.execute("""
                            CREATE TABLE Consensus(
                            Value TEXT PRIMARY KEY NOT NULL,
                            ValuePrev TEXT
                            Slot INTEGER not null,
                            TXs TEXT,
                            TimeWhen INTEGER)
                            """)
                conn.comit()

        except Exception as e:
            print("Error : ", e)
            if conn:
                conn.rollback()
        else:
            pass
        finally:
            if conn:
                conn.close
