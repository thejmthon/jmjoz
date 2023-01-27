from sqlalchemy import Boolean, Column, String

from . import BASE, SESSION


class Locks(BASE):
    __tablename__ = "locks"
    chat_id = Column(String(14), primary_key=True)
    # Booleans are for "is this locked", _NOT_ "is this allowed"
    audio = Column(Boolean, default=False)
    voice = Column(Boolean, default=False)
    contact = Column(Boolean, default=False)
    video = Column(Boolean, default=False)
    document = Column(Boolean, default=False)
    photo = Column(Boolean, default=False)
    sticker = Column(Boolean, default=False)
    gif = Column(Boolean, default=False)
    url = Column(Boolean, default=False)
    bots = Column(Boolean, default=False)
    forward = Column(Boolean, default=False)
    game = Column(Boolean, default=False)
    location = Column(Boolean, default=False)
    rtl = Column(Boolean, default=False)
    button = Column(Boolean, default=False)
    egame = Column(Boolean, default=False)
    inline = Column(Boolean, default=False)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)  # ensure string
        self.audio = False
        self.voice = False
        self.contact = False
        self.video = False
        self.document = False
        self.photo = False
        self.sticker = False
        self.gif = False
        self.url = False
        self.bots = False
        self.forward = False
        self.game = False
        self.location = False
        self.rtl = False
        self.button = False
        self.egame = False
        self.inline = False


Locks.__table__.create(checkfirst=True)


def init_locks(chat_id, reset=False):
    curr_restr = SESSION.query(Locks).get(str(chat_id))
    if reset:
        SESSION.delete(curr_restr)
        SESSION.flush()
    restr = Locks(str(chat_id))
    SESSION.add(restr)
    SESSION.commit()
    return restr


def update_lock(chat_id, lock_type, locked):
    curr_perm = SESSION.query(Locks).get(str(chat_id))
    if not curr_perm:
        curr_perm = init_locks(chat_id)
    if lock_type == "audio":
        curr_perm.audio = locked
    elif lock_type == "voice":
        curr_perm.voice = locked
    elif lock_type == "contact":
        curr_perm.contact = locked
    elif lock_type == "video":
        curr_perm.video = locked
    elif lock_type == "document":
        curr_perm.document = locked
    elif lock_type == "photo":
        curr_perm.photo = locked
    elif lock_type == "sticker":
        curr_perm.sticker = locked
    elif lock_type == "gif":
        curr_perm.gif = locked
    elif lock_type == "url":
        curr_perm.url = locked
    elif lock_type == "bots":
        curr_perm.bots = locked
    elif lock_type == "forward":
        curr_perm.forward = locked
    elif lock_type == "game":
        curr_perm.game = locked
    elif lock_type == "location":
        curr_perm.location = locked
    elif lock_type == "rtl":
        curr_perm.rtl = locked
    elif lock_type == "button":
        curr_perm.button = locked
    elif lock_type == "egame":
        curr_perm.egame = locked
    elif lock_type == "inline":
        curr_perm.inline = locked
    SESSION.add(curr_perm)
    SESSION.commit()


def is_locked(chat_id, lock_type):
    curr_perm = SESSION.query(Locks).get(str(chat_id))
    SESSION.close()
    if not curr_perm:
        return False
    elif lock_type == "sticker":
        return curr_perm.sticker
    elif lock_type == "photo":
        return curr_perm.photo
    elif lock_type == "audio":
        return curr_perm.audio
    elif lock_type == "voice":
        return curr_perm.voice
    elif lock_type == "contact":
        return curr_perm.contact
    elif lock_type == "video":
        return curr_perm.video
    elif lock_type == "document":
        return curr_perm.document
    elif lock_type == "gif":
        return curr_perm.gif
    elif lock_type == "url":
        return curr_perm.url
    elif lock_type == "bots":
        return curr_perm.bots
    elif lock_type == "forward":
        return curr_perm.forward
    elif lock_type == "game":
        return curr_perm.game
    elif lock_type == "location":
        return curr_perm.location
    elif lock_type == "rtl":
        return curr_perm.rtl
    elif lock_type == "button":
        return curr_perm.button
    elif lock_type == "egame":
        return curr_perm.egame
    elif lock_type == "inline":
        return curr_perm.inline


def get_locks(chat_id):
    try:
        return SESSION.query(Locks).get(str(chat_id))
    finally:
        SESSION.close()
