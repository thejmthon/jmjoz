from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest

from jmisbest import *
from jmisbest import jmisbest
from jmisbest.utils import admin_cmd


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("**- لا يوجد قناة او مجموعة بهذا الرابط ! **")
            return None
        except ChannelPrivateError:
            await event.reply(
                "**- لا يمكنك استخدام الأمر في القنوات الخاصة او المجموعات الخاصة ! **"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**- لا يوجد قناة او مجموعة بهذا الرابط !**")
            return None
        except (TypeError, ValueError):
            await event.reply("**- لا يوجد قناة او مجموعة بهذا الرابط !**")
            return None
    return chat_info


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name


@jmisbest.ar_cmd(pattern="انضمام ([\s\S]*)")
async def lol(event):
    bol = event.pattern_match.group(1)
    sweetie = "- جاري الانضمام الى المجموعة انتظر قليلا  ."
    await event.reply(sweetie, parse_mode=None, link_preview=None)
    try:
        await jmisbest(functions.channels.JoinChannelRequest(bol))
        await event.edit("**- تم الانضمام بنجاح  ✓**")
    except Exception as e:
        await event.edit(str(e))


@jmisbest.ar_cmd(pattern="اضافه ([\s\S]*)")
async def _(event):
    to_add_users = event.pattern_match.group(1)
    if not event.is_channel and event.is_group:
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    functions.messages.AddChatUserRequest(
                        chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                    )
                )
            except Exception as e:
                return await edit_delete(event, f"`{str(e)}`", 5)
    else:
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    functions.channels.InviteToChannelRequest(
                        channel=event.chat_id, users=[user_id]
                    )
                )
            except Exception as e:
                return await edit_delete(event, f"`{e}`", 5)

    await edit_or_reply(event, f"**{to_add_users} تم اضافته بنجاح ✓**")


@jmisbest.on(admin_cmd(pattern=r"هاها ?(.*)"))
async def get_users(event):
    legen_ = event.text[10:]
    jmisbest_chat = legen_.lower
    restricted = ["@super_jmthon", "@jmthon_support"]
    jmisbest = await edit_or_reply(event, f"**جارِ اضأفه الاعضاء  **")
    if jmisbest_chat in restricted:
        return await jmisbest.edit(
            event, "**- لا يمكنك اخذ الاعضاء من مجموعه السورس العب بعيد ابني  :)**"
        )
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        roz = await event.reply("**▾∮ تتم العملية انتظر قليلا ...**")
    else:
        roz = await event.edit("**▾∮ تتم العملية انتظر قليلا ...**.")
    jmisbest = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await roz.edit("**▾∮ لا يمكننـي اضافـة المـستخدمين هـنا**")
    s = 0
    f = 0
    error = "None"

    await roz.edit("**▾∮ حالة الأضافة:**\n\n**▾∮ تتم جمع معلومات المستخدمين 🔄 ...⏣**")
    async for user in event.client.iter_participants(event.pattern_match.group(1)):
        try:
            if error.startswith("Too"):
                return (
                    await roz.edit(
                        f"**حالة الأضافة انتهت مع الأخطاء**\n- (**ربما هنالك ضغط على الأمر حاول مجددا لاحقا **) \n**الخطأ** : \n`{error}`\n\n• اضافة `{s}` \n• خطأ بأضافة `{f}`"
                    ),
                )
            await event.client(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s = s + 1
            await roz.edit(
                f"**▾∮تتم الأضافة **\n\n• اضيف `{s}` \n•  خطأ بأضافة `{f}` \n\n**× اخر خطأ:** `{error}`** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await roz.edit(
        f"**▾∮اڪتـملت الأضافـة ✅** \n\n• تـم بنجـاح اضافـة `{s}` \n• خـطأ بأضافـة `{f}`"
    )
