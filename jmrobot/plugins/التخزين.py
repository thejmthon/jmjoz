from jmrobot import jmrobot
from jmrobot.core.logger import logging

from ..Config import Config
from ..helpers.tools import media_type
from ..helpers.utils import _format
from ..sql_helper import no_log_pms_sql
from ..sql_helper.globals import gvarstatus

LOGS = logging.getLogger(__name__)


# no
class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@jmrobot.ar_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def monito_p_m_s(event):  # sourcery no-metrics
    if Config.PM_LOGGER_GROUP_ID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await event.get_sender()
    if sender.id == 1280124974:
        return
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM:
                    if LOG_CHATS_.COUNT > 1:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "رسالة جديدة", f"{LOG_CHATS_.COUNT} رسائل"
                            )
                        )
                    else:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "رسالة جديدة", f"{LOG_CHATS_.COUNT} رسائل"
                            )
                        )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await event.client.send_message(
                    Config.PM_LOGGER_GROUP_ID,
                    f"👤{_format.mentionuser(sender.first_name , sender.id)} قام بأرسال رسالة جديدة \nالايدي : `{chat.id}`",
                )
            try:
                if event.message:
                    await event.client.forward_messages(
                        Config.PM_LOGGER_GROUP_ID, event.message, silent=True
                    )
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))


@jmrobot.ar_cmd(incoming=True, func=lambda e: e.mentioned, edited=False, forword=None)
async def log_tagged_messages(event):
    hmm = await event.get_chat()
    from .afk import AFK_

    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        return
    if (
        (no_log_pms_sql.is_approved(hmm.id))
        or (Config.PM_LOGGER_GROUP_ID == -100)
        or ("on" in AFK_.USERAFK_ON)
        or (await event.get_sender() and (await event.get_sender()).bot)
    ):
        return
    full = None
    try:
        full = await event.client.get_entity(event.message.from_id)
    except Exception as e:
        LOGS.info(str(e))
    messaget = await media_type(event)
    resalt = f"#التاك \n<b>الكروب : </b><code>{hmm.title}</code>"
    if full is not None:
        resalt += (
            f"\n<b>المرسل : </b> 👤{_format.htmlmentionuser(full.first_name , full.id)}"
        )
    if messaget is not None:
        resalt += f"\n<b>نوع الرسالة : </b><code>{messaget}</code>"
    else:
        resalt += f"\n<b>الرسالة : </b>{event.message.message}"
    resalt += f"\n<b>رابط الرسالة: </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> اضغط هنا</a>"
    if not event.is_private:
        await event.client.send_message(
            Config.PM_LOGGER_GROUP_ID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )


@jmrobot.ar_cmd(
    incoming=True,
    func=lambda e: e.is_private and (e.photo or e.video) and e.media_unread,
)
async def tl(e):
    sender = await e.get_sender()
    username = sender.username
    user_id = sender.id
    result = await e.download_media()
    caption = f"ميديا ذاتية التدمير وصلت لك !\n: المرسل @{username}\nالايدي : {user_id}"
    await jmrobot.send_file(Config.PM_LOGGER_GROUP_ID, result, caption=caption)
