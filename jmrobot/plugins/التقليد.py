from jmrobot import jmrobot

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.echo_sql import (
    addecho,
    get_all_echos,
    get_echos,
    is_echo,
    remove_all_echos,
    remove_echo,
    remove_echos,
)
from . import get_user_from_event


@jmrobot.ar_cmd(pattern="تقليد$")
async def echo(event):
    if event.reply_to_msg_id is None:
        return await edit_or_reply(event, "⌔∮ يرجى الرد على الشخص الذي تريد ازعاجه ،")
    jmrobotevent = await edit_or_reply(event, "⌔∮ يتم تفعيل هذا الامر انتظر قليلا ،")
    user, rank = await get_user_from_event(event, jmrobotevent, nogroup=True)
    if not user:
        return
    reply_msg = await event.get_reply_message()
    chat_id = event.chat_id
    user_id = reply_msg.sender_id
    if event.is_private:
        chat_name = user.first_name
        chat_type = "Personal"
    else:
        chat_name = event.chat.title
        chat_type = "Group"
    user_name = user.first_name
    user_username = user.username
    if is_echo(chat_id, user_id):
        return await edit_or_reply(event, "⌔∮ تم تفعيل وضع الازعاج على الشخص بنجاح ✓")
    try:
        addecho(chat_id, user_id, chat_name, user_name, user_username, chat_type)
    except Exception as e:
        await edit_delete(jmrobotevent, f"⌔∮ خطأ\n`{str(e)}`")
    else:
        await edit_or_reply(
            jmrobotevent,
            "**⌔∮ تم تفعيل امر التقليد على هذا الشخص\nسيتم تقليد جميع رسائله هنا**",
        )


@jmrobot.ar_cmd(pattern="الغاء تقليد$")
async def echo(event):
    if event.reply_to_msg_id is None:
        return await edit_or_reply(event, "يجب عليك الرد على المستخدم لتقليد رسائله")
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    chat_id = event.chat_id
    if is_echo(chat_id, user_id):
        try:
            remove_echo(chat_id, user_id)
        except Exception as e:
            await edit_delete(jmrobotevent, f"**خطأ:**\n`{e}`")
        else:
            await edit_or_reply(event, "⌔∮ تم ايقاف التقليد لهذا المستخدم")
    else:
        await edit_or_reply(event, "⌔∮ لم يتم تفعيل التقليد على هذا المستخدم اصلا")


@jmrobot.ar_cmd(pattern="حذف المقلدهم( للكل)?")
async def echo(event):
    input_str = event.pattern_match.group(1)
    if input_str:
        lecho = get_all_echos()
        if len(lecho) == 0:
            return await edit_delete(
                event, "⌔∮ لم يتم تفعيل التقليد حتى لمستخدم واحد اصلا."
            )
        try:
            remove_all_echos()
        except Exception as e:
            await edit_delete(event, f"**خطأ:**\n`{str(e)}`", 10)
        else:
            await edit_or_reply(
                event, "⌔∮ تم حذف تقليد جميع المستخدمين في جميع الدردشات."
            )
    else:
        lecho = get_echos(event.chat_id)
        if len(lecho) == 0:
            return await edit_delete(
                event, "⌔∮ لم يتم تفعيل التقليد حتى لمستخدم واحد اصلا."
            )
        try:
            remove_echos(event.chat_id)
        except Exception as e:
            await edit_delete(event, f"**خطأ:**\n`{e}`", 10)
        else:
            await edit_or_reply(
                event, "∮ تم حذف تقليد جميع المستخدمين في جميع الدردشات."
            )


@jmrobot.ar_cmd(pattern="المقلدهم( للكل)?$")
async def echo(event):
    input_str = event.pattern_match.group(1)
    private_chats = ""
    output_str = "**قائمه الاشخاص المقلدهم:\n\n"
    if input_str:
        lsts = get_all_echos()
        group_chats = ""
        if len(lsts) <= 0:
            return await edit_or_reply(event, "⌔∮ لم يتم تفعيل التقليد بالاصل ")
        for echos in lsts:
            if echos.chat_type == "Personal":
                if echos.user_username:
                    private_chats += (
                        f"⪼ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                    )
                else:
                    private_chats += (
                        f"⪼ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                    )
            elif echos.user_username:
                group_chats += f"⪼ [{echos.user_name}](https://t.me/{echos.user_username}) في دردشة {echos.chat_name} الايدي `{echos.chat_id}`\n"
            else:
                group_chats += f"⪼ [{echos.user_name}](tg://user?id={echos.user_id}) في دردشة {echos.chat_name} الايدي `{echos.chat_id}`\n"

        if private_chats != "":
            output_str += "**الدردشات الخاصة**\n" + private_chats + "\n\n"
        if group_chats != "":
            output_str += "**المجموعات**\n" + group_chats
    else:
        lsts = get_echos(event.chat_id)
        if len(lsts) <= 0:
            return await edit_or_reply(event, "لم يتم تفعيل التقليد بالاصل")

        for echos in lsts:
            if echos.user_username:
                private_chats += (
                    f"⪼ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                )
            else:
                private_chats += (
                    f"⪼ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                )
        output_str = "**الاشخاص الذي تم تقليدهم في هذه الدردشه:\n" + private_chats

    await edit_or_reply(event, output_str)


@jmrobot.ar_cmd(incoming=True, edited=False)
async def samereply(event):
    if is_echo(event.chat_id, event.sender_id) and (
        event.message.text or event.message.sticker
    ):
        await event.reply(event.message)
