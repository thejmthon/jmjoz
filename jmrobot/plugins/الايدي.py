from telethon.utils import pack_bot_file_id

from jmrobot import jmrobot
from jmrobot.core.logger import logging

from ..core.managers import edit_delete, edit_or_reply

LOGS = logging.getLogger(__name__)


@jmrobot.ar_cmd(pattern="الايدي(?:\s|$)([\s\S]*)")
async def _(event):
    if input_str := event.pattern_match.group(2):
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{e}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"ايدي المستخدم `{input_str}` هو `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"ايدي القناة او الدردشة `{p.title}` هو `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**- يجب عليك الرد على رسالة او كتابة المعرف**")
    elif event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"**ايدي الدردشة الحالية : **`{event.chat_id}`\n**ايدي المستخدم: **`{r_msg.sender_id}`\n**ايدي الميديا: **`{bot_api_file_id}`",
            )

        else:
            await edit_or_reply(
                event,
                f"**ايدي الدردشة الحالية : **`{event.chat_id}`\n**ايدي المستخدم: **`{r_msg.sender_id}`",
            )

    else:
        await edit_or_reply(event, f"**ايدي الدردشة الحالية : **`{event.chat_id}`")
