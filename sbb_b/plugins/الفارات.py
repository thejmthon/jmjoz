import urllib3

from sbb_b import sbb_b

from ..core.logger import logging
from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

# from ..Config import Config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGS = logging.getLogger(__name__)


@sbb_b.ar_cmd(pattern="اعادة تشغيل$", disable_errors=True)
async def _(event):
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#اعادة_التشغيل \n" "تم اعادة تشغيل البوت"
        )
    jmthon = await edit_or_reply(
        event,
        "**❃ جارِ اعادة تشغيل السورس\nارسل** `.فحص` **او** `.الاوامر` **للتحقق مما إذ كان البوت شغال ، يستغرق الأمر في الواقع 1-2 دقيقة لإعادة التشغيل**",
    )
    await event.client.reload(jmthon)
