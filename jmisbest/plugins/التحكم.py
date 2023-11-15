import os
from datetime import datetime

from telethon.utils import get_display_name

from jmisbest import jmisbest
from jmisbest.core.logger import logging

from .. import *
from ..Config import Config
from ..core.data import _sudousers_list
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import get_user_from_event, mentionuser
from ..sql_helper import global_collectionjson as sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus


@jmisbest.ar_cmd(pattern="اوامر التحكم")
async def hi(event):
    await edit_or_reply(
        event,
        "**[ . ᯏ𝖩𝗆𝗍𝗁𝗈ꪀ - ᥴ𝗆𝖽 ᭡ .](t.me/jmthon)**\n✦┅━╍━╍╍━━╍━━╍━┅✦\n\n• اوامر التحكم تتيح لمستخدم اخر ان يستخدم اوامر تنصيبك وهو غير منصب جمثون حيث سيصبح متحكم في اوامر تنصيبك يرجى الانتباه من انه سيحصل على صلاحيات الاوامر  وقد يسبب خطورة لك اذا كنت لا تثق في المستخدم الذي اضفته. \n\n\n`.التحكم` تفعيل/تعطيل\n• تستخدم هذه الميزة لتفعيل/لتعطيل خاصية التحكم بأوامر تنصيبك للمستخدمين الذين أضفتهم في قائمة المتحكمين\n\n`.المتحكمين`\n• لعرض المستخدمين الذين اضفتهم الى قائمة المستخدمين المتحكمين\n\n`.اضف متحكم`\n• بالرد على المستخدم لأضافته متحكم في تنصيب جمثون الخاص بك\n\n`.ازالة متحكم`\n• بالرد على المستخدم لازالته من قائمة المتحكمين",
        link_preview=False,
    )


LOGS = logging.getLogger(__name__)
ENV = bool(os.environ.get("ENV", False))


async def _init() -> None:
    sudousers = _sudousers_list()
    Config.SUDO_USERS.clear()
    for user_d in sudousers:
        Config.SUDO_USERS.add(user_d)


def get_key(val):
    for key, value in PLG_INFO.items():
        for cmd in value:
            if val == cmd:
                return key
    return None


@jmisbest.ar_cmd(pattern="التحكم (تفعيل|تعطيل)$")
async def chat_blacklist(event):
    input_str = event.pattern_match.group(1)
    sudousers = _sudousers_list()
    if input_str == "تفعيل":
        if gvarstatus("sudoenable") is not None:
            return await edit_delete(event, "**- ميزة التحكم مُفعلة بالأصل**")
        addgvar("sudoenable", "true")
        text = "**- تم بنجاح تفعيل ميزة التحكم**\n"
        if len(sudousers) != 0:
            text += (
                "**جار الان اعادة التشغيل لتطبيق التغيير يرجى الأنتظار بعض الدقائق**"
            )
            msg = await edit_or_reply(
                event,
                text,
            )
            return await event.client.reload(msg)
        text += "**انت لم تقم باضافة اي شخص الى قائمة المتحكمين بالأصل ارسل `.اوامر التحكم`**"
        return await edit_or_reply(
            event,
            text,
        )
    if gvarstatus("sudoenable") is not None:
        delgvar("sudoenable")
        text = "**تم بنجاح تعطيل ميزة التحكم**\n"
        if len(sudousers) != 0:
            text += (
                "**جار الان اعادة التشغيل لتطبيق التغيير يرجى الأنتظار بعض الدقائق**"
            )
            msg = await edit_or_reply(
                event,
                text,
            )
            return await event.client.reload(msg)
        text += "**انت لم تقم باضافة اي شخص الى قائمة المتحكمين بالأصل ارسل `.اوامر التحكم`**"
        return await edit_or_reply(
            event,
            text,
        )
    await edit_delete(event, "**- ميزة التحكم بالأصل مُعطلة**")


@jmisbest.ar_cmd(pattern="اضف متحكم(?:\s|$)([\s\S]*)")
async def add_sudo_user(event):
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    if replied_user.id == event.client.uid:
        return await edit_delete(event, "**- لا يمكنك أضافة نفسك كمستخدم متحكم**")
    if replied_user.id in _sudousers_list():
        return await edit_delete(
            event,
            f"• المستخدم {mentionuser(get_display_name(replied_user),replied_user.id)}\n • في قائمة التحكم بالأصل",
        )
    date = str(datetime.now().strftime("%B %d, %Y"))
    userdata = {
        "chat_id": replied_user.id,
        "chat_name": get_display_name(replied_user),
        "chat_username": replied_user.username,
        "date": date,
    }
    try:
        sudousers = sql.get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    sudousers[str(replied_user.id)] = userdata
    sql.del_collection("sudousers_list")
    sql.add_collection("sudousers_list", sudousers, {})
    output = f"• المستخدم {mentionuser(userdata['chat_name'],userdata['chat_id'])}\n • تم اضافته في قائمة المستخدمين المتحكمين\n"
    output += "**جار الان اعادة التشغيل لتطبيق التغيير يرجى الأنتظار بعض الدقائق**"
    msg = await edit_or_reply(event, output)
    await event.client.reload(msg)


@jmisbest.ar_cmd(pattern="ازالة متحكم(?:\s|$)([\s\S]*)")
async def _(event):
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    try:
        sudousers = sql.get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    if str(replied_user.id) not in sudousers:
        return await edit_delete(
            event,
            f"• المستخدم {mentionuser(get_display_name(replied_user),replied_user.id)}\n• ليس في قائمة المتحكمين اصلا",
        )
    del sudousers[str(replied_user.id)]
    sql.del_collection("sudousers_list")
    sql.add_collection("sudousers_list", sudousers, {})
    output = f"• المستخدم {mentionuser(get_display_name(replied_user),replied_user.id)}\n• تم حذفه من قائمة المتحكمين\n"
    output += "**جار الان اعادة التشغيل لتطبيق التغيير يرجى الأنتظار بعض الدقائق**"
    msg = await edit_or_reply(event, output)
    await event.client.reload(msg)


@jmisbest.ar_cmd(pattern="المتحكمين$")
async def _(event):
    sudochats = _sudousers_list()
    try:
        sudousers = sql.get_collection("sudousers_list").json
    except AttributeError:
        sudousers = {}
    if len(sudochats) == 0:
        return await edit_delete(
            event, "**• يبدو انك لم تقوم بأضافة مستخدم متحكم لجمثون الخاص بك**"
        )
    result = "**قائمة المستخدمين المتحكمين بتنصيب جمثون :**\n\n"
    for chat in sudochats:
        result += f"**• الأسم:** {mentionuser(sudousers[str(chat)]['chat_name'],sudousers[str(chat)]['chat_id'])}\n"
        result += f"**• ايدي الدردشة :** `{chat}`\n"
        username = f"@{sudousers[str(chat)]['chat_username']}" or "غير معرف"
        result += f"**• المعرف :** {username}\n"
        result += f"• تم اضافته على {sudousers[str(chat)]['date']}\n\n"
    await edit_or_reply(event, result)


jmisbest.loop.create_task(_init())
