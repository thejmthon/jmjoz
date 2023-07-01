from datetime import datetime
from math import sqrt

from emoji import emojize
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    MessageActionChannelMigrateFrom,
)
from telethon.utils import get_input_location

from jmrobot import jmrobot

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)


@jmrobot.ar_cmd(pattern="المشرفين(?: |$)(.*)")
async def _(event):
    mentions = "**⌔∮ مشرفين هذه المجموعة  ✪**: \n"
    reply_message = await reply_id(event)
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if input_str:
        mentions = f"**⪼ مشرفين في → :** {input_str} **من المجموعات ⌂ :** \n"
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, str(e))
    else:
        chat = to_write_chat
        if not event.is_group:
            return await edit_or_reply(event, "**⌔∮ هذه ليست مجموعة ✕**")
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if not x.deleted and isinstance(x.participant, ChannelParticipantCreator):
                mentions += "\n - [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
        mentions += "\n"
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if x.deleted:
                mentions += "\n `{}`".format(x.id)
            else:
                if isinstance(x.participant, ChannelParticipantAdmin):
                    mentions += "\n- [{}](tg://user?id={}) `{}`".format(
                        x.first_name, x.id, x.id
                    )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_message)
    await event.delete()


@jmrobot.ar_cmd(pattern="البوتات(?: |$)(.*)")
async def _(event):
    mentions = "**⌔∮ البوتات في هذه المجموعة 🝰 : ** \n"
    input_str = event.pattern_match.group(1)
    if not input_str:
        chat = await event.get_input_chat()
    else:
        mentions = "**⌔∮ البوتات في {} من المجموعات 🝰 : ** \n".format(input_str)
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_or_reply(event, str(e))
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsBots
        ):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n - [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await edit_or_reply(event, mentions)


@jmrobot.ar_cmd(pattern="الاعضاء(?: |$)(.*)")
async def get_users(show):
    mentions = "**مستخدمين هذه المجموعة**: \n"
    await reply_id(show)
    input_str = show.pattern_match.group(1)
    if input_str:
        mentions = "**⌔∮ الأعضاء في {} من المجموعات 𖤍  :** \n".format(input_str)
        try:
            chat = await show.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(show, f"`{str(e)}`", 10)
    else:
        if not show.is_group:
            return await edit_or_reply(show, "**⌔∮ هذه ليست مجموعة ✕**")
    jmrobotevent = await edit_or_reply(show, "**⌔∮ جاري سحب قائمة معرّفات الأعضاء 🝛**")
    try:
        if show.pattern_match.group(1):
            async for user in show.client.iter_participants(chat.id):
                if user.deleted:
                    mentions += f"\n**⌔∮ الحسابات المحذوفة ⌦** `{user.id}`"
                else:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
        else:
            async for user in show.client.iter_participants(show.chat_id):
                if user.deleted:
                    mentions += f"\n**⌔∮ الحسابات المحذوفة ⌦** `{user.id}`"
                else:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await edit_or_reply(jmrobotevent, mentions)


@jmrobot.ar_cmd(pattern="معلومات(?: |$)(.*)")
async def info(event):
    jmrobotevent = await edit_or_reply(event, "**⪼ يتمّ جلب معلومات الدردشة، إنتظر ⅏**")
    chat = await get_chatinfo(event, jmrobotevent)
    caption = await fetch_info(chat, event)
    try:
        await jmrobotevent.edit(caption, parse_mode="html")
    except Exception as e:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, f"**⌔∮ هناك خطأ في معلومات الدردشة ✕ : **\n`{str(e)}`"
            )
        await jmrobotevent.edit("**⌔∮ حدث خطأ ما، يرجى التحقق من الأمر ⎌**")


async def get_chatinfo(event, jmrobotevent):
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
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await jmrobotevent.edit("**⌔∮ لم يتمّ العثور على القناة/المجموعة ✕**")
            return None
        except ChannelPrivateError:
            await jmrobotevent.edit(
                "**⌔∮ هذه مجموعة أو قناة خاصة أو لقد تمّ حظري منه ⛞**"
            )
            return None
        except ChannelPublicGroupNaError:
            await jmrobotevent.edit("**⌔∮ القناة أو المجموعة الخارقة غير موجودة ✕**")
            return None
        except (TypeError, ValueError) as err:
            await jmrobotevent.edit(str(err))
            return None
    return chat_info


async def fetch_info(chat, event):  # sourcery no-metrics
    # chat.chats is a list so we use get_entity() to avoid IndexError
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    broadcast = (
        chat_obj_info.broadcast if hasattr(chat_obj_info, "broadcast") else False
    )
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat_obj_info.title
    warn_emoji = emojize(":warning:")
    try:
        msg_info = await event.client(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        LOGS.error(f"Exception: {str(e)}")

    first_msg_valid = bool(
        msg_info and msg_info.messages and msg_info.messages[0].id == 1
    )

    creator_valid = bool(first_msg_valid and msg_info.users)
    msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Deleted Account"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and isinstance(msg_info.messages[0].action, MessageActionChannelMigrateFrom)
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    try:
        dc_id, location = get_input_location(chat.full_chat.chat_photo)
    except Exception:
        dc_id = "Unknown"

    # this is some spaghetti I need to change
    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    members_online = (
        chat.full_chat.online_count if hasattr(chat.full_chat, "online_count") else 0
    )
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    exp_count = chat.full_chat.pts if hasattr(chat.full_chat, "pts") else None
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info  # this is a list
    bots = 0
    supergroup = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "megagroup") and chat_obj_info.megagroup
        else "No"
    )
    slowmode = (
        "<b>مفعل</b>"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "غير مفعل"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "<b>نعم</b>"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "لا"
    )
    verified = (
        "<b>موثق</b>"
        if hasattr(chat_obj_info, "verified") and chat_obj_info.verified
        else "غير موثق"
    )
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None
    # end of spaghetti block

    if admins is None:
        # use this alternative way if chat.full_chat.admins_count is None,
        # works even without being an admin
        try:
            participants_admins = await event.client(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            LOGS.error(f"Exception:{str(e)}")
    if bots_list:
        for _ in bots_list:
            bots += 1

    caption = "<b>⌔∮ معلومات الدردشة  🝢 :</b>\n"
    caption += f"⪼ الآيدي  : <code>{chat_obj_info.id}</code>\n"
    if chat_title is not None:
        caption += f"⌔∮ إسم المجموعة  :{chat_title}\n"
    if former_title is not None:  # Meant is the very first title
        caption += f"⌔∮ الإسم السابق  : {former_title}\n"
    if username is not None:
        caption += f"⌔∮ نوع المجموعة ⌂ : مجموعة عامّة  \n"
        caption += f"⌔∮ الرابط  : \n {username}\n"
    else:
        caption += f"⌔∮ نوع المجموعة ⌂ : مجموعة عامّة  \n"
    if creator_username is not None:
        caption += f"⌔∮ المالك  :  {creator_username}\n"
    elif creator_valid:
        caption += (
            '⌔∮ المالك  : <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n'
        )
    if created is not None:
        caption += f"⌔∮ تاريخ الإنشاء  : \n <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"⌔∮ الإنتاج  :   <code>{chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}</code> {warn_emoji}\n"
    caption += f"⪼ آ يدي قاعدة البيانات : {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"⌔∮ الأعضاء : <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"⌔∮ الرسائل التي يمڪن مشاهدتها : <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"⌔∮ الرسائل المرسلة  :<code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += (
            f"⌔∮ الرسائل المرسلة: <code>{messages_sent_alt}</code> {warn_emoji}\n"
        )
    if members is not None:
        caption += f"⌔∮ الأعضاء : <code>{members}</code>\n"
    if admins is not None:
        caption += f"⌔∮ المشرفين : <code>{admins}</code>\n"
    if bots_list:
        caption += f"⌔∮ البوتات : <code>{bots}</code>\n"
    if members_online:
        caption += f"⌔∮ المتصلين حالياً : <code>{members_online}</code>\n"
    if restrcited_users is not None:
        caption += f"⌔∮ الأعضاء المقيّدين : <code>{restrcited_users}</code>\n"
    if banned_users is not None:
        caption += f"⌔∮ الأعضاء المحظورين : <code>{banned_users}</code>"
    if group_stickers is not None:
        caption += f'{chat_type} ⪼ الملصقات : <a href="t.me/addstickers/{chat.full_chat.stickerset.short_name}">{group_stickers}</a>'
    caption += "\n"
    if not broadcast:
        caption += f"⌔∮ الوضع البطيئ : {slowmode}"
        if (
            hasattr(chat_obj_info, "slowmode_enabled")
            and chat_obj_info.slowmode_enabled
        ):
            caption += f", <code>{slowmode_time}s</code>\n"
        else:
            caption += "\n"
        caption += f"⌔∮ المجموعة الخارقة  : {supergroup}\n"
    if hasattr(chat_obj_info, "restricted"):
        caption += f"⌔∮ المقيّد : {restricted}"
        if chat_obj_info.restricted:
            caption += f"> : {chat_obj_info.restriction_reason[0].platform}\n"
            caption += f"> ⌔∮  السبب  : {chat_obj_info.restriction_reason[0].reason}\n"
            caption += f"> ⌔∮ النّص  : {chat_obj_info.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "⪼ السارقين : <b>Yes</b>\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"⌔∮ الحسابات الموثقة   : {verified}\n"
    if description:
        caption += f"⪼ الوصف  : \n<code>{description}</code>\n"
    return caption
