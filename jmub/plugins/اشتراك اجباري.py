from telethon import events
from telethon.errors import ChatAdminRequiredError
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

from jmub import jmub

from ..sql_helper.fsub_sql import add_fsub, all_fsub, is_fsub, rm_fsub
from . import edit_delete, edit_or_reply


async def check_join(channel, user_id):
    try:
        await jmub(GetParticipantRequest(channel, int(user_id)))
        return True
    except UserNotParticipantError:
        return False
    except:
        return False


@jmub.ar_cmd(pattern="اجباري ?(.*)")
async def fsub(event):
    if not event.is_group:
        return await edit_or_reply(event, "**يستخدم هذا الامر فقط في المجموعة**")
    if event.is_group:
        perm = await event.client.get_permissions(event.chat_id, event.sender_id)
        if not perm.is_admin:
            return await edit_or_reply(
                event, "أنت لست مشرف في هذه المجموعة يجب ان تكون مشرف اولا"
            )
    jmthon = event.text.split(None, 1)[1]
    if not jmthon:
        return await edit_or_reply(event, "**- يجب عليك وضع معرف القناة اولا**")
    if jmthon.startswith("@"):
        channel = jmthon
    else:
        try:
            channel_entity = await event.client.get_entity(channel)
        except:
            return await edit_or_reply(
                event, "⚠️ **خطأ !** \n\nيجب عليك وضع معرف القناة بشكل صحيح "
            )
        channel = channel_entity.username
        try:
            if not channel_entity.broadcast:
                return await event.reply("هذه القناة غير صالحة .")
        except:
            return await event.reply("يجب وضع المعرف بشكل صحيح.")
        if not await check_join(channel, jmub.uid):
            return await event.reply(
                f"❗**أنا لست ادمن في هذه القناة**\n [القناة](https://t.me/{channel}). يجب ان اكون مشرف في القناة اولا.",
                link_preview=False,
            )
        add_fsub(event.chat_id, str(channel))
        await edit_or_reply(
            event, "**- تم بنجاح تفعيل الاشتراك الاجباري  ** للقناة @{channel}. ✅"
        )


@jmub.ar_cmd(pattern="حذف الاجباري")
async def removefsub(event):
    ashtrakmh = rm_fsub(event.chat_id)
    if not ashtrakmh:
        return await edit_delete(
            event, "**- الاشتراك الاجباري غير مفعل في هذه المجموعة**"
        )
    await edit_or_reply(event, "**- تم بنجاح تعطيل الاشتراك الاجباري في هذه المجموعة**")


@jmub.on(events.NewMessage())
async def fsub_n(e):
    if all_fsub() == None:
        return
    if e.is_private:
        return
    if e.chat.admin_rights:
        if not e.chat.admin_rights.ban_users:
            return
    if not is_fsub(e.chat_id):
        return
    user = await e.get_user()
    if user.jmub:
        return
    if not e.from_id:
        return
    chatdb = is_fsub(e.chat_id)
    channel = chatdb.channel
    try:
        check = await check_join(channel, e.sender_id)
    except ChatAdminRequiredError:
        return
    if not check:
        txt = f'اهلا بك عزيزي المستخدم <a href="tg://user?id={e.sender_id}">{e.sender.first_name}</a>\n يجب عليك الاشتراك في قناة المجموعة اولا\nبعدها ستتمكن من التكلمة بحرية - <a href="t.me/{channel}">اضغط هنا</a>'
        await e.reply(txt, parse_mode="html", link_preview=False)
        await e.delete()
