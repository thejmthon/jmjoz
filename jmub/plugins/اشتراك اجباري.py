import re

from telethon import Button, events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.events import CallbackQuery, InlineQuery
from telethon.tl.functions.channels import GetParticipantRequest

from jmub import jmub

from ..Config import Config
from ..sql_helper.fsub_sql import add_fsub, all_fsub, is_fsub, rm_fsub
from . import edit_delete, edit_or_reply


@jmub.ar_cmd(pattern="اجباري ?(.*)")
async def subscribe(event):
    if not event.is_group:
        await edit_or_reply, (event, "**- يستخدم هذا الامر فقط في المجموعات**")
        return
    jmthon = event.pattern_match.group(1)
    if not jmthon:
        return await edit_delete(event, "**- يجب عليك وضع معرف القناة او الايدي**")
    if jmthon.startswith("@"):
        ch = jmthon
    else:
        try:
            ch = int(jmthon)
        except BaseException:
            return await edit_delete(
                event, "⚠️ **خطأ !** \n\nيجب عليك وضع معرف القناة مع @ او فقط الايدي"
            )
    try:
        jmthon = (await jmub.get_entity(ch)).id
    except BaseException:
        return await edit_or_reply(
            event, "⚠️ **خطأ !** \n\nيجب عليك وضع معرف القناة مع @ او فقط الايدي"
        )
    if not str(jmthon).startswith("-100"):
        jmthon = int("-100" + str(jmthon))
    add_fsub(event.chat_id, jmthon)
    await edit_or_reply(event, "**- تم بنجاح تفعيل الاشتراك الاجباري لهذه القناة**")


@jmub.ar_cmd(pattern="حذف الاشتراك")
async def removefsub(event):
    ashtrakmh = rm_fsub(event.chat_id)
    if not ashtrakmh:
        return await edit_delete(
            event, "**- الاشتراك الاجباري غير مفعل في هذه المجموعة**"
        )
    await edit_or_reply(e, "**- تم بنجاح تعطيل الاشتراك الاجباري في هذه المجموعة**")


@jmub.ar_cmd(pattern="قنوات الاشتراك")
async def list(event):
    channels = all_fsub()
    ch_listrz = "**🚀 الاشتراك الاجباري مفعل في  :**\n"
    if len(channels) > 0:
        for jmthon in channels:
            ch_listrz += f"[{jmthon.title}](https://t.me/ + {jmthon.username})\n"
    else:
        ch_listrz = "**- لم يتم تفعيل الاشتراك مع اي مجموعة**"
    await edit_or_reply(event, ch_listrz)


@jmub.tgbot.on(InlineQuery)
async def subsc(event):
    builder = event.builder
    query = event.text
    if event.query.user_id == jmub.uid and query == "اجباري":
        jmthon = event.pattern_match.group(1).strip()
        muhmd = jmthon.split("_")
        user = await jmub.get_entity(int(muhmd[0]))
        channel = await jmub.get_entity(int(muhmd[1]))
        msg = f"**👋 أهلا** [{user.first_name}](tg://user?id={user.id}), \n\n**عليك الاشتراك في ** {channel.title} **للتحدث في هذه المجموعة.**"
        if not channel.username:
            link = (await jmub(ExportChatInviteRequest(channel))).link
        else:
            link = "https://t.me/" + channel.username
        subsc = [
            await builder.article(
                title="force_sub",
                text=msg,
                buttons=[
                    [Button.url(text="اشترك الان", url=link)],
                    [Button.url(text="🔓 الغاء الكتم", data=unmute)],
                ],
            )
        ]
        await event.answer(subsc)


@jmub.tgbot.on(CallbackQuery(data=re.compile(b"unmute")))
async def on_pm_click(event):
    jmthon = (event.data_match.group(1)).decode("UTF-8")
    muhmd = jmthon.split("+")
    if not event.sender_id == int(muhmd[0]):
        return await event.answer("هذه الرسالة ليست لك غبي", alert=True)
    try:
        await jmub(GetParticipantRequest(int(muhmd[1]), int(muhmd[0])))
    except UserNotParticipantError:
        return await event.answer("عليك الاشتراك اولا  :)", alert=True)
    await jmub.edit_permissions(
        event.chat_id, int(muhmd[0]), send_message=True, until_date=None
    )
    await event.edit("**- تم بنجاح الغاء كتمك يمكنكا التحدث الان**")


@jmub.on(events.ChatAction())
async def forcesub(event):
    if all_fsub() == None:
        return
    if not (event.user_joined or event.user_added):
        return
    if not is_fsub(event.chat_id):
        return
    user = await event.get_user()
    if user.jmub:
        return
    joinchat = is_fsub(event.chat_id)
    tgbotusername = Config.TG_BOT_USERNAME
    try:
        await jmub(GetParticipantRequest(int(joinchat), user.id))
    except UserNotParticipantError:
        await jmub.edit_permissions(event.chat_id, user.id, send_messages=False)
        res = await jmub.inline_query(tgbotusername, f"اجباري {user.id}+{joinchat}")
        await res[0].click(event.chat_id, reply_to=event.action_message.id)
