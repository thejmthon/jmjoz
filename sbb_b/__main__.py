import contextlib
import sys

import sbb_b
from sbb_b import BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from .Config import Config
from .core.logger import logging
from .core.session import sbb_b
from .utils import (
    add_bot_to_logger_group,
    load_plugins,
    mybot,
    saves,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("سورس جمثون")

cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("يتم بدء البوت المساعد")
    sbb_b.loop.run_until_complete(setup_bot())
    LOGS.info("اكتملت عمليه البوت المساعد")
except Exception as e:
    LOGS.error(f"{e}")
    sys.exit()

try:
    LOGS.info("يتم تفعيل وضع حمايه الحساب من الاختراق")
    sbb_b.loop.create_task(saves())
    LOGS.info("تم تفعيل وضع حمايه الحساب من الاختراق")
except Exception as bb:
    LOGS.error(f"- {bb}")
    sys.exit()


try:
    LOGS.info("يتم تفعيل وضع الانلاين")
    sbb_b.loop.run_until_complete(mybot())
    LOGS.info("تم تفعيل وضع الانلاين بنجاح ✓")
except Exception as meo:
    LOGS.error(f"- {meo}")
    sys.exit()


async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print("============================================================")
    print("تم انتهاء عملية التنصيب بنجاح ")
    print(
        f"لمعرفة اوامر السورس ارسل {cmdhr}الاوامر\
        \nمجموعة قناة السورس  https://t.me/jmthon_support"
    )
    print("============================================================")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    return


sbb_b.loop.run_until_complete(startup_process())

if len(sys.argv) in {1, 3, 4}:
    with contextlib.suppress(ConnectionError):
        sbb_b.run_until_disconnected()
else:
    sbb_b.disconnect()
