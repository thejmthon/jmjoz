import asyncio

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from ..sql_helper import antiflood_sql as sql
from ..utils import is_admin
from . import edit_or_reply, jmrobot

CHAT_FLOOD = sql.__load_flood_settings()

ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True
)


@jmrobot.ar_cmd(incoming=True, groups_only=True)
async def _(event):
    if not CHAT_FLOOD:
        return
    jmthonadmin = await is_admin(event.client, event.chat_id, event.client.uid)
    if not jmthonadmin:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.sender_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception as e:
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message=f"**⌔∮ تنبيه التكرار للادمنية ⚠️**\n\n**▾∮ الى** @admin **المجموعة!**\n**▾∮ قام↫** [المستخدم](tg://user?id={event.message.sender_id})\n**▾∮بتكرار رسائله في المجموعة**\x1f`{e}`",
            reply_to=event.message.id,
        )

        await asyncio.sleep(4)
        await no_admin_privilege_message.edit(
            "**⌔∮هذا هو الشخص الذي قام بالتكرار \n توقف لكي لا تًطرد 📵**"
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message=f"**⌔∮ عملية التقيد التلقائي للتكرار ⚠️**\n\n**▾ قام ↫**[المستخدم ](tg://user?id={event.message.sender_id})\n**▾∮تم تقييده تلقائيًا بسبب عبوره حد السماح بالتكرار في هذه المجموعة**",
            reply_to=event.message.id,
        )


@jmrobot.ar_cmd(
    pattern="ضع التكرار(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def _(event):
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "**- تم بنجاح تحديث عدد التكرار**")
    await asyncio.sleep(2)
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await event.edit(f"**- تم تحديث التكرار الى {input_str} في الدردشة الحالية**")
    except Exception as e:
        await event.edit(str(e))
