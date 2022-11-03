import base64
import os

try:
    import ipaddress
except ModuleNotFoundError:
    os.system("pip3 install ipaddress")
    import ipaddress

import struct
import sys

from telethon.sessions.string import _STRUCT_PREFORMAT, CURRENT_VERSION, StringSession

from ..core.logger import logging

# https://github.com/pyrogram/pyrogram/blob/master/docs/source/faq/what-are-the-ip-addresses-of-telegram-data-centers.rst
_PYRO_FORM = {351: ">B?256sI?", 356: ">B?256sQ?", 362: ">BI?256sQ?"}

LOGS = logging.getLogger("سورس جمثون")

DC_IPV4 = {
    1: "149.154.175.53",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.130",
}


def bothseesion(session, logger=LOGS, _exit=True):
    if session:
        # كود التيليثون
        if session.startswith(CURRENT_VERSION):
            if len(session.strip()) != 353:
                logger.exception("كود سيشن تيليثون غير صحيح يرجى وضعه بشكل صحيح")
                sys.exit()
            return StringSession(session)
        # كود البايروجرام
        elif len(session) in _PYRO_FORM.keys():
            if len(session) in [351, 356]:
                dc_id, _, auth_key, _, _ = struct.unpack(
                    _PYRO_FORM[len(session)],
                    base64.urlsafe_b64decode(session + "=" * (-len(session) % 4)),
                )
            else:
                dc_id, _, _, auth_key, _, _ = struct.unpack(
                    _PYRO_FORM[len(session)],
                    base64.urlsafe_b64decode(session + "=" * (-len(session) % 4)),
                )
            return StringSession(
                CURRENT_VERSION
                + base64.urlsafe_b64encode(
                    struct.pack(
                        _STRUCT_PREFORMAT.format(4),
                        dc_id,
                        ipaddress.ip_address(DC_IPV4[dc_id]).packed,
                        443,
                        auth_key,
                    )
                ).decode("ascii")
            )
        else:
            logger.exception("كود سيشن تيليثون غير صحيح يرجى وضعه بشكل صحيح")
            if _exit:
                sys.exit()
    logger.exception("لم يتم ايجاد كود سيشن لذلك توقفت العملية")
    if _exit:
        sys.exit()
