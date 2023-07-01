import asyncio
import contextlib

from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)
from telethon.utils import get_display_name

from jmrobot import jmrobot

from ..core.data import _sudousers_list
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID

PP_TOO_SMOL = "**- الصورة صغيرة جدا**"
PP_ERROR = "**فشل اثناء معالجة الصورة**"
NO_ADMIN = "**- عذرا انا لست مشرف هنا**"
NO_PERM = "**- ليست لدي صلاحيات كافيه في هذه الدردشة**"
CHAT_PP_CHANGED = "**- تم تغيير صورة الدردشة**"
INVALID_MEDIA = "**- ابعاد الصورة غير صالحة**"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


@jmrobot.ar_cmd(
    pattern="الصورة( -وضع| -حذف)$",
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):
    flag = (event.pattern_match.group(1)).strip()
    if flag == "-وضع":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edit_delete(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edit_delete(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edit_delete(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edit_delete(event, PP_ERROR)
            except Exception as e:
                return await edit_delete(event, f"**خطأ : **`{str(e)}`")
            process = "تحديثها"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**خطأ : **`{e}`")
        process = "حذفها"
        await edit_delete(event, "**تم بنجاح حذف صورة المجموعة**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "صورة المجموعة\n"
            f"صورة المجموعة تم بنجاح {process} "
            f"الدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@jmrobot.ar_cmd(
    pattern="رفع مشرف(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def promote(event):
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=False,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "مشرف"
    if not user:
        return
    jmthonevent = await edit_or_reply(event, "** جار رفع المستخدم يرجى الانتظار**")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await jmthonevent.edit(NO_PERM)
    await jmthonevent.edit("**- تم بنجاح رفع المستخدم مشرف في الدردشة**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"رفع مشرف\
            \nالمستخدم: [{user.first_name}](tg://user?id={user.id})\
            \nالدردشة: {get_display_name(await event.get_chat())} (`{event.chat_id}`)",
        )


@jmrobot.ar_cmd(
    pattern="تنزيل مشرف(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    user, _ = await get_user_from_event(event)
    if not user:
        return
    jmthonevent = await edit_or_reply(event, "**- جار تنزيل المستخدم من الاشراف**")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "مشرف"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await jmthonevent.edit(NO_PERM)
    await jmthonevent.edit("**- تم بنجاح تنزيله من رتبة المشرفين**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"تنزيل مشرف\
            \nالمستخدم: [{user.first_name}](tg://user?id={user.id})\
            \nالدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@jmrobot.ar_cmd(
    pattern="حظر(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def _ban_person(event):
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == 1280124974:
        return await edit_delete(event, "**- لا يمكنك حظر مطور السورس محمد****")
    if user.id == event.client.uid:
        return await edit_delete(event, "**- عزيزي المستخدم لا يمكنك حظر نفسك**")
    jmthonevent = await edit_or_reply(event, "- تم حظر المستخدم من الدردشة بنجاح")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await jmthonevent.edit(NO_PERM)
    reply = await event.get_reply_message()
    if reason:
        await jmthonevent.edit(
            f"المستخدم :{_format.mentionuser(user.first_name ,user.id)}\nتم حظر المستخدم****\n**السبب : **`{reason}`"
        )
    else:
        await jmthonevent.edit(
            f"المستخدم {_format.mentionuser(user.first_name ,user.id)} \nتم حظر المستخدم****"
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"الحظر \
                \nالمستخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \nالسبب: {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"الحظر\
                \nالمستخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            return await jmthonevent.edit(
                "**- ليس لدي بعض الصلاحيات لكنه ما زال محظور**"
            )


@jmrobot.ar_cmd(
    pattern="الغاء حظر(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    user, _ = await get_user_from_event(event)
    if not user:
        return
    jmthonevent = await edit_or_reply(event, "**- جار الغاء حظر المستخدم**")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await jmthonevent.edit(
            f"المستخدم :{_format.mentionuser(user.first_name ,user.id)} تم الغاء حظره بنجاح"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "الغاء حظر\n"
                f"المستخدم: [{user.first_name}](tg://user?id={user.id})\n"
                f"الدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await jmthonevent.edit("- لقد حدث خطأ اثناء الغاء حظر المستخدم")
    except Exception as e:
        await jmthonevent.edit(f"**خطأ :**\n`{e}`")


@jmrobot.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@jmrobot.ar_cmd(pattern="كتم(?:\s|$)([\s\S]*)")
async def startgmute(event):
    if event.is_private:
        await event.edit("**⌔∮ ربما ستحدث بعض الاخطاء و المشاكل**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == jmrobot.uid:
            return await edit_or_reply(event, "**⌔∮ عذرا لا يمكنني كتم نفسي **")
        userid = user.id
    try:
        user = await event.client.get_entity(userid)
    except Exception:
        return await edit_or_reply(
            event, "**⌔∮ لا يمكنني الحصول على معلومات من هذا المستخدم**"
        )
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"**⪼ المستخدم**: {_format.mentionuser(user.first_name ,user.id)}\n**مكتوم بالاصل**",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خطأ**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"**⪼ المستخدم:  {_format.mentionuser(user.first_name ,user.id)}\nتم كتمه بنجاح\nالسبب: {reason}**",
            )
        else:
            await edit_or_reply(
                event,
                f"**⪼ المستخدم: {_format.mentionuser(user.first_name ,user.id)}\nتم كتمه بنجاح**",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الكتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**السبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الكتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)


@jmrobot.ar_cmd(pattern="الغاء كتم(?:\s|$)([\s\S]*)")
async def endgmute(event):
    if event.is_private:
        await event.edit("**⌔∮ قد تحدث بعض الاخطاء و المشاكل**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == jmrobot.uid:
            return await edit_or_reply(event, "⌔∮ عذرا لا يمكنني كتم نفسي اصلا")
        userid = user.id
    try:
        user = await event.client.get_entity(userid)
    except Exception:
        return await edit_or_reply(
            event, "**⌔∮ لا يمكنني الحصول على معلومات من هذا المستخدم**"
        )
    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"**⪼ المستخدم:  {_format.mentionuser(user.first_name ,user.id)}\nغير مكتوم اصلا** ",
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خطأ**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"**⪼ المستخدم:  {_format.mentionuser(user.first_name ,user.id)}\nتم الغاء كتمه بنجاح ✓\nالسبب :{reason}**",
            )
        else:
            await edit_or_reply(
                event,
                f"**⪼ المستخدم:  {_format.mentionuser(user.first_name ,user.id)}\nتم الغاء كتمه بنجاح ✓**",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغاء_كتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**السبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغاء_كتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )


@jmrobot.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


@jmrobot.ar_cmd(
    pattern="طرد(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def kick(event):
    user, reason = await get_user_from_event(event)
    if not user:
        return
    jmthonevent = await edit_or_reply(event, "**- جار طرد المستخدم من الدردشة**")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await jmthonevent.edit(f"{NO_PERM}\n{e}")
    if reason:
        await jmthonevent.edit(
            f"تم طرد [{user.first_name}](tg://user?id={user.id})\nالسبب: {reason}"
        )
    else:
        await jmthonevent.edit(f"تم طرد[{user.first_name}](tg://user?id={user.id})")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "الطرد\n"
            f"المستخدم: [{user.first_name}](tg://user?id={user.id})\n"
            f"الدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\n",
        )


@jmrobot.ar_cmd(
    pattern="تثبيت( بالاشعار|$)",
)
async def pin(event):
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edit_delete(
            event, "**- يجب عليك الرد على الرسالة التي تريد تثبيتها**", 5
        )
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{e}`", 5)
    await edit_delete(event, "- تم تثبيت الرسالة بنجاح", 3)
    sudo_users = _sudousers_list()
    if event.sender_id in sudo_users:
        with contextlib.suppress(BadRequestError):
            await event.delete()
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"التثبيت\
                \nتم تثبيت رسالى في مجموعة\
                \nالمجموعة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \nالدردشة: {is_silent}",
        )


@jmrobot.ar_cmd(pattern="الغاء تثبيت( الكل|$)")
async def unpin(event):
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "الكل":
        return await edit_delete(
            event,
            "**- يجب عليك الرد على الرسالة المراد الغاء تثبيتها او اكتب `.الغاء تثبيت الكل` لألغاء تثبيت جميع الرسائل",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "الكل":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edit_delete(
                event,
                "**- يجب عليك الرد على الرسالة المراد الغاء تثبيتها او اكتب `.الغاء تثبيت الكل` لألغاء تثبيت جميع الرسائل",
                5,
            )
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{e}`", 5)
    await edit_delete(event, "- تم بنجاح الغاء التثبيت", 3)
    sudo_users = _sudousers_list()
    if event.sender_id in sudo_users:
        with contextlib.suppress(BadRequestError):
            await event.delete()
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"التثبيت\
                \nتم بنجاح الغاء تثبيت الرسالة اوالرسائل في الدردشة\
                \nالدرردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@jmrobot.ar_cmd(
    pattern="الاحداث( -ج)?(?: |$)(\d*)?",
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):
    jmthonevent = await edit_or_reply(
        event, "**- جار البحث على اخر الاحداث في الدردشة**"
    )
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        lim = min(lim, 15)
        if lim <= 0:
            lim = 1
    else:
        lim = 5
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**اخر  {lim} رسائل محذوفة في الدردشة هي:**"
    if not flag:
        for msg in adminlog:
            ruser = await event.client.get_entity(msg.old.from_id)
            _media_type = await media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n- {msg.old.message}\n**المرسل:** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n- {_media_type}\n**المرسل:**{_format.mentionuser(ruser.first_name ,ruser.id)}"
        await edit_or_reply(jmthonevent, deleted_msg)
    else:
        main_msg = await edit_or_reply(jmthonevent, deleted_msg)
        for msg in adminlog:
            ruser = await event.client.get_entity(msg.old.from_id)
            _media_type = await media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"{msg.old.message}\n**المرسل:** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"{msg.old.message}\n**المرسل:** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )
