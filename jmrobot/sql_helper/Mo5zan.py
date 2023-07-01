try:
    from . import BASE, SESSION
except ImportError as e:
    raise Exception("Hello!") from e

from sqlalchemy import Column, String


class Mo5zan(BASE):
    __tablename__ = "mo5zan"
    sender = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.sender = str(sender)


Mo5zan.__table__.create(checkfirst=True)


def is_mo5zan(sender_id):
    try:
        return SESSION.query(Mo5zan).get(str(sender_id)) is not None
    except BaseException:
        return None
    finally:
        SESSION.close()


def addmo5zan(sender):
    adder = Mo5zan(str(sender))
    SESSION.add(adder)
    SESSION.commit()


def unmo5zan(sender):
    if rem := SESSION.query(Mo5zan).get((str(sender))):
        SESSION.delete(rem)
        SESSION.commit()
