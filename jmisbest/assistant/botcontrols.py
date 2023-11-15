import asyncio
from datetime import datetime

from telethon.errors import BadRequestError, FloodWaitError, ForbiddenError

from jmisbest import jmisbest as sbb_b

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id, time_formatter
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list, get_all_bl_users
from ..sql_helper.bot_starters import del_starter_from_db, get_all_starters
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from .botmanagers import (
    ban_user_from_bot,
    get_user_and_reason,
    progress_str,
    unban_user_from_bot,
)

LOGS = logging.getLogger(__name__)

botusername = Config.TG_BOT_USERNAME
cmhd = Config.COMMAND_HAND_LER


@sbb_b.bot_cmd(pattern="^اوامري$", from_users=Config.OWNER_ID)
async def bot_help(event):
    await event.reply(
        "**▾∮ قائمه اوامر المطور **\n* تستخدم في ↫ `{botusername} ` فقط! `\n**⍣ⵧⵧⵧⵧⵧᴊᴍᴛʜᴏɴⵧⵧⵧⵧⵧ⍣**\n\n*الامر  ( اذاعة  ) \n- لعمل اذاعة لمستخدمي البوت ◛ ↶\n**⋆ قم بالرد ع الرسالة لاذاعتها للمستخدمين ↸**\n\n*الامر ( ايدي ) \n- لمعرفة الملصقات المرسلة ↶\n**⋆ بالرد ع المستخدم لجلب معلوماتة **\n\n*الامر ( حظر + سبب )\n- لحظر مستخدم من البوت \n**⋆ بالرد ع المستخدم مع سبب مثل **\n**حظر @RR9R7 قمت بازعاجي**\n\n* الامر ( الغاء حظر ) \n لالغاء حظر المستخدم من البوت √\n**⋆ الامر والمعرف والسبب (اختياري) مثل **\n**الغاء حظر @RR9R7 + السبب اختياري**\n\n**⋆ الامر ( المحظورين )\n- لمعرفة المحظورين من البوت  **\n\n**⋆ امر ( المستخدمين ) \n- لمعرفة مستخدمين بوتك  **\n\n**⋆ الاوامر ( التكرار + تفعيل / تعطيل ) \n- تشغيل وايقاف التكرار (في البوت) ↶**\n* عند التشغيل يحظر المزعجين تلقائيًا ⊝\n\n**⋆ امر ( تاك + الكلام ) \n- لعمل تاك للاعضاء يجب ااضافة البوت المساعد في المجموعة اولا و رفعه مشرف\n\n**⋆ امر ( تنظيف ) \n- اضف البوت مشرف بعدها قم بالرد على اي رسالة واكتب تنظيف وسيقوم بحذف الرسائل التي تحتها\n\n⋆ امر ( مسح ) \n- اضف البوت مشرف بعدها قم بالرد على اي رسالة واكتب مسك وسيقوم بحذف الرسالة****\n\n\n**⍣ⵧⵧⵧⵧⵧᴊᴍᴛʜᴏɴⵧⵧⵧⵧⵧ⍣**\n𝙅𝙈𝙏𝙃𝙊𝙉 𝙐𝙎𝙀𝙍𝘽𝙊𝙏 🧸♥"
    )


@sbb_b.bot_cmd(pattern="^اذاعة$", from_users=Config.OWNER_ID)
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("**- يجب عليم الرد على رسالة اولا لعمل اذاعة**")
    start_ = datetime.now()
    br_cast = await replied.reply("**- جار الاذاعة الان أنتظر قليلا**")
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply("عدد مستخدمين البوت : 0 لم يتم الاذاعة")
    users = get_all_starters()
    if users is None:
        return await event.reply("**- حدث خطأ اثناء التعرف على مستخدمين البوت**")
    for user in users:
        try:
            await event.client.send_message(int(user.user_id), replied)
            await asyncio.sleep(0.8)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except (BadRequestError, ValueError, ForbiddenError):
            del_starter_from_db(int(user.user_id))
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID, f"**لقد حدث خطأ أثناء الاذاعة للمستخدمين**\n`{e}`"
                )

        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        "🔊 جار الاذاعة ...\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n• ✔️ **نجح** :  `{count}`\n"
                        + f"• ✖️ **فشل** :  `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
    end_ = datetime.now()
    b_info = f"🔊  تم بنجاح الأرسال الى ➜  <b>{count} من المستخدمين.</b>"
    if blocked_users:
        b_info += f"\n🚫  <b>{len(blocked_users)} من المستخدمين</b> قاموا بحظر البوت لذلك تم حذفهم من قاعدة البيانات."
    b_info += (
        f"\n⏳  <code>العملية أخذت : {time_formatter((end_ - start_).seconds)}</code>."
    )
    await br_cast.edit(b_info, parse_mode="html")


@sbb_b.bot_cmd(pattern="^اذع$", from_users=Config.OWNER_ID)
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("**- يجب عليم الرد على رسالة اولا لعمل اذاعة**")
    start_ = datetime.now()
    br_cast = await replied.reply("**- جار الاذاعة الان أنتظر قليلا**")
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply("عدد مستخدمين البوت : 0 لم يتم الاذاعة")
    users = get_all_starters()
    if users is None:
        return await event.reply("**- حدث خطأ اثناء التعرف على مستخدمين البوت**")
    for user in users:
        try:
            message = await event.client.send_message(int(user.user_id), replied)
            await asyncio.sleep(0.8)
            await message.delete()
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except (BadRequestError, ValueError, ForbiddenError):
            del_starter_from_db(int(user.user_id))
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID, f"**لقد حدث خطأ أثناء الاذاعة للمستخدمين**\n`{e}`"
                )

        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        "🔊 جار الاذاعة ...\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n• ✔️ **نجح** :  `{count}`\n"
                        + f"• ✖️ **فشل** :  `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
    end_ = datetime.now()
    b_info = f"🔊  تم بنجاح الأرسال الى ➜  <b>{count} من المستخدمين.</b>"
    if blocked_users:
        b_info += f"\n🚫  <b>{len(blocked_users)} من المستخدمين</b> قاموا بحظر البوت لذلك تم حذفهم من قاعدة البيانات."
    b_info += (
        f"\n⏳  <code>العملية أخذت : {time_formatter((end_ - start_).seconds)}</code>."
    )
    await br_cast.edit(b_info, parse_mode="html")


@sbb_b.ar_cmd(pattern="^المستخدمين$")
async def ban_starters(event):
    ulist = get_all_starters()
    if len(ulist) == 0:
        return await edit_delete(event, "**لا يوجد مستخدمين في بوتك**")
    msg = "**قائمة الاحصائيات الخاصة ببوتك :\n\n**"
    for user in ulist:
        msg += f"**المستخدم** {_format.mentionuser(user.first_name , user.user_id)}\n**الايدي:** `{user.user_id}`\n**المعرف:** @{user.username}\n**التاريخ: **__{user.date}__\n\n"
    await edit_or_reply(event, msg)


@sbb_b.bot_cmd(pattern="^حظر\\s+([\\s\\S]*)", from_users=Config.OWNER_ID)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "يجب عليك تحديد المستخدم الذي تريد حظره", reply_to=reply_to
        )
    if not reason:
        return await event.client.send_message(
            event.chat_id, "يجب عليك وضع سبب الحظر مع الامر", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**خطأ:**\n`{e}`")
    if user_id == Config.OWNER_ID:
        return await event.reply("لا يمكنني حظر مالك البوت")
    if check := check_is_black_list(user.id):
        return await event.client.send_message(
            event.chat_id,
            f"محظور أصلا\
            \nالمستخدم في قائمة المحظورين أصلا.\
            \n**سبب الحظر:** `{check.reason}`\
            \n**التاريخ:** `{check.date}`.",
        )
    msg = await ban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@sbb_b.bot_cmd(pattern="^الغاء حظر(?:\\s|$)([\\s\\S]*)", from_users=Config.OWNER_ID)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id,
            "يجب عليك تحديد المستخدم الذي تريد الغاء حظره",
            reply_to=reply_to,
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**خطأ:**\n`{e}`")
    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"غير محظور أصلا\
            \nالمستخدم:{_format.mentionuser(user.first_name , user.id)} لم يتم حظره أصلا.",
        )
    msg = await unban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@sbb_b.ar_cmd(pattern="^المحظورين$")
async def ban_starters(event):
    ulist = get_all_bl_users()
    if len(ulist) == 0:
        return await edit_delete(event, "لا يوجد شخص محظور في بوتك")
    msg = "**قائمة المستخدمين المحظورين في بوتك :\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name , user.chat_id)}\n**الايدي:** `{user.chat_id}`\n**المعرف:** @{user.username}\n**التاريخ: **__{user.date}__\n**السبب:** __{user.reason}__\n\n"
    await edit_or_reply(event, msg)


@sbb_b.ar_cmd(pattern="التكرار (تفعيل|تعطيل)$")
async def ban_antiflood(event):
    input_str = event.pattern_match.group(1)
    if input_str == "تفعيل":
        if gvarstatus("bot_antif") is not None:
            return await edit_delete(event, "**وضع منع التكرار مفعل بالأصل**")
        addgvar("bot_antif", True)
        await edit_delete(event, "** تم تفعيل منع التكرار بنجاح**")
    elif input_str == "تعطيل":
        if gvarstatus("bot_antif") is None:
            return await edit_delete(event, "** تم تعطيل منع التكرار بنجاح**")
        delgvar("bot_antif")
        await edit_delete(event, "**وضع منع التكرار معطل بالأصل**")
