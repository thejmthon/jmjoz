try:
    from . import BASE, SESSION
except ImportError as e:
    raise Exception("Hello!") from e

from sqlalchemy import Column, String


class MOrakb(BASE):
    __tablename__ = "morakb"
    sender = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.sender = str(sender)


MOrakb.__table__.create(checkfirst=True)


def is_morakb(sender_id):
    try:
        return SESSION.query(MOrakb).get(str(sender_id)) is not None
    except BaseException:
        return None
    finally:
        SESSION.close()


def addmorakb(sender):
    adder = MOrakb(str(sender))
    SESSION.add(adder)
    SESSION.commit()


def unmorakb(sender):
    if rem := SESSION.query(MOrakb).get((str(sender))):
        SESSION.delete(rem)
        SESSION.commit()
