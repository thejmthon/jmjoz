import contextlib
from asyncio import sleep

from telethon import events, functions, types
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.errors.rpcerrorlist import UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from jmisbest import jmisbest

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.locks_sql import get_locks, is_locked, update_lock
from ..utils import is_admin
from . import BOTLOG, BOTLOG_CHATID

ANTI_DDDD_JMTHON_MODE = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
)


async def is_admin(event, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        if sed.is_admin:
            is_mod = True
        else:
            is_mod = False
    except:
        is_mod = False
    return is_mod


@jmisbest.ar_cmd(pattern="قفل ?(.*)", groups_only=True, require_admin=True)
async def _(event):
    input_str = event.pattern_match.group(1)
    chat_id = event.chat_id
    if not event.is_group:
        return await edit_delete(event, "** - يستخدم الامر في المجموعات فقط*")
    (await event.get_chat()).default_banned_rights
    if input_str == "البوتات":
        update_lock(chat_id, "bots", True)
        return await edit_or_reply(
            event, "**• تم قفل البوتات بنجاح ✅**\n\n**• خاصية الطرد والتحذير**"
        )
    if input_str == "المعرفات":
        update_lock(chat_id, "button", True)
        return await edit_or_reply(
            event, "**• تم قفل المعرفات بنجاح ✅**\n\n**• خاصية المسح والتحذير**"
        )
    if input_str == "الدخول":
        update_lock(chat_id, "location", True)
        return await edit_or_reply(
            event, "**• تم قفل الدخول بنجاح ✅**\n\n**• خاصية الطرد والتحذير**"
        )
    if input_str == "الفارسيه" or input_str == "الفارسية":
        update_lock(chat_id, "egame", True)
        return await edit_or_reply(
            event, "**• تم قفل الفارسية بنجاح ✅**\n\n**• خاصية المسح والتحذير**"
        )
    if input_str == "الاضافه" or input_str == "الاضافة":
        update_lock(chat_id, "contact", True)
        return await edit_or_reply(
            event, "**• تم قفل الاضافة بنجاح ✅**\n\n**• خاصية الطرد والتحذير**"
        )
    if input_str == "التوجيه":
        update_lock(chat_id, "forward", True)
        return await edit_or_reply(
            event, "**• تم قفل التوجيه بنجاح ✅**\n\n**• خاصية المسح والتحذير**"
        )
    if input_str == "الميديا":
        update_lock(chat_id, "game", True)
        return await edit_or_reply(
            event, "**• تم قفل الميديا بنجاح ✅**\n\n**• خاصية المسح بالتقييد والتحذير**"
        )
    if input_str == "الانلاين":
        update_lock(chat_id, "inline", True)
        return await edit_or_reply(
            event, "**• تم قفل الانلاين بنجاح ✅**\n\n**• خاصية المسح والتحذير**"
        )
    if input_str == "الفشار" or input_str == "السب":
        update_lock(chat_id, "rtl", True)
        return await edit_or_reply(
            event, "**• تم قفل الفشار بنجاح ✅**\n\n**• خاصية المسح والتحذير**"
        )
    if input_str == "الروابط":
        update_lock(chat_id, "url", True)
        return await edit_or_reply(
            event, "**• تم قفل الروابط بنجاح ✅**\n\n**• خاصية المسح والتحذير**"
        )
    if input_str == "الكل":
        update_lock(chat_id, "bots", True)
        update_lock(chat_id, "game", True)
        update_lock(chat_id, "forward", True)
        update_lock(chat_id, "egame", True)
        update_lock(chat_id, "rtl", True)
        update_lock(chat_id, "url", True)
        update_lock(chat_id, "contact", True)
        update_lock(chat_id, "location", True)
        update_lock(chat_id, "button", True)
        update_lock(chat_id, "inline", True)
        update_lock(chat_id, "video", True)
        update_lock(chat_id, "sticker", True)
        update_lock(chat_id, "voice", True)
        return await edit_or_reply(
            event,
            "**• تم قفل الكل بنجاح ✅**\n\n**• خاصية المسح - الطرد - التقييد - التحذير**",
        )
    else:
        if input_str:
            return await edit_delete(
                event, f"**• عذراً لايوجد امر ب اسم :** `{input_str}`", time=10
            )

        return await edit_or_reply(event, "**• عذرا عزيزي لايمكنك قفل اي شي هنا**")


@jmisbest.ar_cmd(pattern="فتح ?(.*)", groups_only=True, require_admin=True)
async def _(event):
    if event.text[1:].startswith("فتح تعديل الميديا"):
        return
    input_str = event.pattern_match.group(1)
    chat_id = event.chat_id
    if not event.is_group:
        return await edit_delete(event, "** - يستخدم الامر في المجموعات فقط*")
    (await event.get_chat()).default_banned_rights
    if input_str == "البوتات":
        update_lock(chat_id, "bots", False)
        return await edit_or_reply(event, "**• تم فتح** البوتات **بنجاح ✅ **")
    if input_str == "الدخول":
        update_lock(chat_id, "location", False)
        return await edit_or_reply(event, "**• تم فتح** الدخول **بنجاح ✅ **")
    if input_str == "الاضافه" or input_str == "الاضافة":
        update_lock(chat_id, "contact", False)
        return await edit_or_reply(event, "**• تم فتح** الاضافة **بنجاح ✅ **")
    if input_str == "التوجيه":
        update_lock(chat_id, "forward", False)
        return await edit_or_reply(event, "**• تم فتح** التوجيه **بنجاح ✅ **")
    if input_str == "الفارسيه" or input_str == "الفارسية":
        update_lock(chat_id, "egame", False)
        return await edit_or_reply(event, "**• تم فتح** الفارسية **بنجاح ✅ **")
    if input_str == "الفشار" or input_str == "السب":
        update_lock(chat_id, "rtl", False)
        return await edit_or_reply(event, "**• تم فتح** السب والفشار **بنجاح ✅ **")
    if input_str == "الروابط":
        update_lock(chat_id, "url", False)
        return await edit_or_reply(event, "**• تم فتح** الروابط **بنجاح ✅ **")
    if input_str == "الميديا":
        update_lock(chat_id, "game", False)
        return await edit_or_reply(event, "**• تم فتح** الميديا **بنجاح ✅ **")
    if input_str == "المعرفات":
        update_lock(chat_id, "button", False)
        return await edit_or_reply(event, "**• تم فتح** المعرفات **بنجاح ✅ **")
    if input_str == "الانلاين":
        update_lock(chat_id, "inline", False)
        return await edit_or_reply(event, "**• تم فتح** الانلاين **بنجاح ✅ **")
    if input_str == "الكل":
        update_lock(chat_id, "bots", False)
        update_lock(chat_id, "game", False)
        update_lock(chat_id, "forward", False)
        update_lock(chat_id, "egame", False)
        update_lock(chat_id, "rtl", False)
        update_lock(chat_id, "url", False)
        update_lock(chat_id, "contact", False)
        update_lock(chat_id, "location", False)
        update_lock(chat_id, "button", False)
        update_lock(chat_id, "inline", False)
        update_lock(chat_id, "video", False)
        update_lock(chat_id, "sticker", False)
        update_lock(chat_id, "voice", False)
        return await edit_or_reply(event, "**• تم فتح** الكل **بنجاح ✅ **")
    if input_str == "الفارسيه":
        update_lock(chat_id, "egame", False)
        return await edit_or_reply(event, "**• تم فتح** الفارسية **بنجاح ✅ **")
    else:
        if input_str:
            return await edit_delete(
                event, f"**• عذراً لايوجد امر ب اسم :** `{input_str}`", time=10
            )

        return await edit_or_reply(
            event, "**• عذراً عزيزي لايمكنك اعادة فتح اي شي هنا**"
        )


@jmisbest.ar_cmd(pattern="الاعدادات$", groups_only=True)
async def _(event):
    res = ""
    current_jmthon_locks = get_locks(event.chat_id)
    if not current_jmthon_locks:
        res = "**• اعدادات اوامر الحماية في المجموعة:**"
    else:
        res = "**- اعدادات اوامر الحماية في المجموعة::** \n"
        ubots = "❌" if current_jmthon_locks.bots else "✅"
        uegame = "❌" if current_jmthon_locks.egame else "✅"
        urtl = "❌" if current_jmthon_locks.rtl else "✅"
        uforward = "❌" if current_jmthon_locks.forward else "✅"
        ubutton = "❌" if current_jmthon_locks.button else "✅"
        uurl = "❌" if current_jmthon_locks.url else "✅"
        ugame = "❌" if current_jmthon_locks.game else "✅"
        ulocation = "❌" if current_jmthon_locks.location else "✅"
        ucontact = "❌" if current_jmthon_locks.contact else "✅"
        ubutton = "❌" if current_jmthon_locks.button else "✅"
        uinline = "❌" if current_jmthon_locks.inline else "✅"
        res += f"**•  البوتات :** {ubots}\n"
        res += f"**•  الدخول :** {ulocation}\n"
        res += f"**•  الاضافه :** {ucontact}\n"
        res += f"**•  التوجيه :** {uforward}\n"
        res += f"**•  الميديا :** {ugame}\n"
        res += f"**•  المعرفات :** {ubutton}\n"
        res += f"**•  الفارسية :** {uegame}\n"
        res += f"**•  الفشار :** {urtl}\n"
        res += f"**•  الروابط :** {uurl}\n"
        res += f"**•  الانلاين :** {uinline}\n"
    current_chat = await event.get_chat()
    with contextlib.suppress(AttributeError):
        current_chat.default_banned_rights
    await edit_or_reply(event, res)


@jmisbest.ar_cmd(incoming=True, forword=None)
async def check_incoming_messages(event):
    if not event.is_group:
        return
    if event.is_group:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    devs = (1694386561, 1280124974)
    R0R77 = event.sender_id
    razan = jmisbest.uid
    bad = event.message.text
    chat_id = event.chat_id
    if is_locked(chat_id, "rtl") and (
        "خرا" in bad
        or "كسها" in bad
        or "كسمك" in bad
        or "كسختك" in bad
        or "عيري" in bad
        or "كسخالتك" in bad
        or "خرا بالله" in bad
        or "عير بالله" in bad
        or "كسخواتكم" in bad
        or "اختك" in bad
        or "بڪسسخخت" in bad
        or "كحاب" in bad
        or "مناويج" in bad
        or "كحبه" in bad
        or " كواد " in bad
        or "كواده" in bad
        or "تبياته" in bad
        or "تبياتة" in bad
        or "فرخ" in bad
        or "كحبة" in bad
        or "فروخ" in bad
        or "طيز" in bad
        or "آإيري" in bad
        or "اختج" in bad
        or "سالب" in bad
        or "موجب" in bad
        or "فحل" in bad
        or "كسي" in bad
        or "كسك" in bad
        or "كسج" in bad
        or "مكوم" in bad
        or "نيج" in bad
        or "نتنايج" in bad
        or "مقاطع" in bad
        or "ديوث" in bad
        or "دياث" in bad
        or "اديث" in bad
        or "محارم" in bad
        or "سكس" in bad
        or "مصي" in bad
        or "اعرب" in bad
        or "أعرب" in bad
        or "قحب" in bad
        or "قحاب" in bad
        or "عراب" in bad
        or "مكود" in bad
        or "عربك" in bad
        or "مخنث" in bad
        or "مخنوث" in bad
        or "فتال" in bad
        or "زاني" in bad
        or "زنا" in bad
        or "لقيط" in bad
        or "بنات شوارع" in bad
        or "بنت شوارع" in bad
        or "نيك" in bad
        or "منيوك" in bad
        or "منيوج" in bad
        or "نايك" in bad
        or "قواد" in bad
        or "زب" in bad
        or "اير" in bad
        or "ممحو" in bad
        or "بنت شارع" in bad
        or " است " in bad
        or "اسات" in bad
        or "زوب" in bad
        or "عيير" in bad
        or "املس" in bad
        or "مربرب" in bad
        or " خول " in bad
        or "عرص" in bad
        or "قواد" in bad
        or "اهلاتك" in bad
        or "جلخ" in bad
        or "ورع" in bad
        or "شرمو" in bad
        or "فرك" in bad
        or "رهط" in bad
    ):
        if R0R77 == razan or await is_admin(event, R0R77) or R0R77 in devs:
            return
        else:
            try:
                await event.delete()
                await event.reply(
                    "**• عذراً**  [عزيزي ⚠️](tg://user?id={})\n**• يمنع السب واستخدام الالفاظ البذيئه**".format(
                        R0R77
                    )
                )
            except Exception as e:
                await event.reply(
                    "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(str(e))
                )
                update_lock(chat_id, "rtl", False)
    if is_locked(chat_id, "game") and event.message.media:
        if R0R77 == razan or await is_admin(event, R0R77) or R0R77 in devs:
            return
        else:
            try:
                await event.delete()
                await event.reply(
                    "**• عذراً**  [عزيزي ⚠️](tg://user?id={})\n**يُمنع ارسال الوسائط لـ هذه المجموعة •**\n\n**• تم تقييدك تلقائياً من ارسال الوسائط**\n**• يمكنك التكلم فقط الان".format(
                        event.sender_id
                    )
                )
                await event.client(
                    EditBannedRequest(
                        event.chat_id, event.sender_id, ANTI_DDDD_JMTHON_MODE
                    )
                )
            except Exception as e:
                await event.reply(
                    "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(str(e))
                )
                update_lock(chat_id, "game", False)
    if is_locked(chat_id, "forward") and event.fwd_from:
        if R0R77 == razan or await is_admin(event, R0R77) or R0R77 in devs:
            return
        else:
            try:
                await event.delete()
                await event.reply(
                    "**• عذراً**  [عزيزي ⚠️](tg://user?id={})\n**يمنع التوجيه لهذه المجموعة **".format(
                        R0R77
                    )
                )
            except Exception as e:
                await event.reply(
                    "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(str(e))
                )
                update_lock(chat_id, "forward", False)
    if is_locked(chat_id, "button") and "@" in bad:
        if R0R77 == razan or await is_admin(event, R0R77) or R0R77 in devs:
            return
        else:
            try:
                await event.delete()
                await event.reply(
                    "**• عذراً**  [عزيزي ⚠️](tg://user?id={})\n**يمنع إرسال المعرفات ل هذه المجموعة **".format(
                        R0R77
                    )
                )
            except Exception as e:
                await event.reply(
                    "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(str(e))
                )
                update_lock(chat_id, "button", False)
    if is_locked(chat_id, "egame") and (
        "فارسى" in bad
        or "خوببی" in bad
        or "میخوام" in bad
        or "کی" in bad
        or "پی" in bad
        or "گ" in bad
        or "خسته" in bad
        or "صكص" in bad
        or "راحتی" in bad
        or "بیام" in bad
        or "بپوشم" in bad
        or "گرمه" in bad
        or "چ" in bad
        or "چه" in bad
        or "ڬ" in bad
        or "ٺ" in bad
        or "چ" in bad
        or "ڿ" in bad
        or "ڇ" in bad
        or "ڀ" in bad
        or "ڎ" in bad
        or "ݫ" in bad
        or "ژ" in bad
        or "ڟ" in bad
        or "۴" in bad
        or "زدن" in bad
        or "دخترا" in bad
        or "كسى" in bad
        or "مک" in bad
        or "خالى" in bad
        or "ݜ" in bad
        or "ڸ" in bad
        or "پ" in bad
        or "بند" in bad
        or "عزيزم" in bad
        or "برادر" in bad
        or "باشى" in bad
        or "ميخوام" in bad
        or "خوبى" in bad
        or "ميدم" in bad
        or "كى اومدى" in bad
        or "خوابيدين" in bad
    ):
        if R0R77 == razan or await is_admin(event, R0R77) or R0R77 in devs:
            return
        else:
            try:
                await event.delete()
                await event.reply(
                    "**• عذراً**  [عزيزي ⚠️](tg://user?id={})\n**يُمنع الكلام الفارسي في هذه المجموعة **".format(
                        R0R77
                    )
                )
            except Exception as e:
                await event.reply(
                    "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(str(e))
                )
                update_lock(chat_id, "egame", False)
    if is_locked(chat_id, "url") and "http" in bad:
        if R0R77 == razan or await is_admin(event, R0R77) or R0R77 in devs:
            return
        else:
            try:
                await event.delete()
                await event.reply(
                    "**• عذراً**  [عزيزي ⚠️](tg://user?id={})\n**يُمنع ارسال الروابط لهذه المجموعة **".format(
                        R0R77
                    )
                )
            except Exception as e:
                await event.reply(
                    "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(str(e))
                )
                update_lock(chat_id, "url", False)
    if is_locked(chat_id, "inline") and event.message.via_bot:
        if R0R77 == razan or await is_admin(event, R0R77) or R0R77 in devs:
            return
        else:
            try:
                await event.delete()
                await event.reply(
                    "**• عذراً**  [عزيزي ⚠️](tg://user?id={})\n**يُمنع استخدام الانلاين في هذه المجموعة **".format(
                        R0R77
                    )
                )
            except Exception as e:
                await event.reply(
                    "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(str(e))
                )
                update_lock(chat_id, "inline", False)


@jmisbest.on(events.ChatAction())
async def _(event):
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return

    devs = (1694386561, 1280124974)
    razan = jmisbest.uid
    if not is_locked(event.chat_id, "contact"):
        return
    if event.user_added:
        jasem = event.action_message.sender_id
        jmthon = await event.client.get_permissions(event.chat_id, jasem)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await event.client.get_entity(user_id)
            if event.user_added:
                is_ban_able = True
                if jasem == razan or jmthon.is_admin or jasem in devs:
                    return
                else:
                    try:
                        await event.client(
                            functions.channels.EditBannedRequest(
                                event.chat_id, user_obj, rights
                            )
                        )
                        await event.reply(
                            "**• عذراً**  [عزيزي ⚠️](tg://user?id={})\n**يُمنع اضافة الاعضاء ل هذه المجموعة •**\n\n**• تم حظر العضو المضاف .. بنجاح 🛂**".format(
                                jasem
                            )
                        )
                    except Exception as e:
                        await event.reply(
                            "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(
                                str(e)
                            )
                        )
                        update_lock(event.chat_id, "contact", False)
                        break
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.reply(
                "**• عزيزي المالك**\n\n**• قام هذا** [الشخص](tg://user?id={})\n**• باضافة اشخاص للمجموعة**\n**• تم تحذير الشخص وطرد الاعضاء المضافين .. بنجاح ✓**".format(
                    jasem
                )
            )


@jmisbest.on(events.ChatAction())
async def _(event):
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return

    devs = (1895219306, 925972505)
    if not is_locked(event.chat_id, "egame"):
        return
    if event.user_joined:
        a_user = await event.get_user()
        first = a_user.first_name
        last = a_user.last_name
        f"{first} {last}" if last else first
        thejmthon = await event.client.get_entity(event.user_id)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        if event.user_joined and (
            "ژ" in first
            or "چ" in first
            or "۴" in first
            or "مهسا" in first
            or "sara" in first
            or "گ" in first
            or "نازنین" in first
            or "آسمان" in first
            or "ڄ" in first
            or "پ" in first
            or "Sanaz" in first
            or "𝓈𝒶𝓇𝒶" in first
            or "سارة" in first
            or "GIRL" in first
            or " Lady " in first
            or "فتاة" in first
            or "👅" in first
            or "سمانه" in first
            or "بهار" in first
            or "maryam" in first
            or "👙" in first
            or "هانیه" in first
            or "هستی" in first
            or "💋" in first
            or "ندا" in first
            or "Mina" in first
            or "خانم" in first
            or "ایناز" in first
            or "مبینا" in first
            or "امینی" in first
            or "سرنا" in first
            or "اندیشه" in first
            or "لنتكلم" in first
            or "دریا" in first
            or "زاده" in first
            or "نااز" in first
            or "ناز" in first
            or "بیتا" in first
            or "سكس" in first
            or "💄" in first
            or "اعرب" in first
            or "أعرب" in first
            or "قحب" in first
            or "قحاب" in first
            or "عراب" in first
            or "مكود" in first
            or "عربك" in first
            or "مخنث" in first
            or "مخنوث" in first
            or "فتال" in first
            or "زاني" in first
            or "زنا" in first
            or "لقيط" in first
            or "بنات شوارع" in first
            or "بنت شوارع" in first
            or "نيك" in first
            or "منيوك" in first
            or "منيوج" in first
            or "نايك" in first
            or "قواد" in first
            or "زب" in first
            or "اير" in first
            or "ممحو" in first
            or "بنت شارع" in first
            or " است " in first
            or "اسات" in first
            or "زوب" in first
            or "عيير" in first
            or "املس" in first
            or "مربرب" in first
            or " خول " in first
            or "عرص" in first
            or "قواد" in first
            or "اهلاتك" in first
            or "جلخ" in first
            or "ورع" in first
            or "شرمو" in first
            or "فرك" in first
            or "رهط" in first
        ):
            is_ban_able = True
            if thejmthon.id in devs:
                return
            else:
                try:
                    await event.client(
                        functions.channels.EditBannedRequest(
                            event.chat_id, thejmthon.id, rights
                        )
                    )
                    await event.reply(
                        "• **  [العضو⚠️](tg://user?id={})\n**يمنع انضمام الفارسيين هنا •**\n\n**• تم حظره .. بنجاح 🛂**".format(
                            thejmthon.id
                        )
                    )
                except Exception as e:
                    await event.reply(
                        "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(str(e))
                    )
                    update_lock(event.chat_id, "egame", False)
                    return
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.reply(
                "• ** [عزيزي](tg://user?id={}) **يمنع دخول الفارسيين لهذه المجموعة **".format(
                    thejmthon.id
                )
            )


@jmisbest.on(events.ChatAction())
async def _(event):
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return

    devs = (1694386561, 1280124974)
    if not is_locked(event.chat_id, "location"):
        return
    if event.user_joined:
        thejmthon = await event.client.get_entity(event.user_id)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        if event.user_joined:
            is_ban_able = True
            if thejmthon.id in devs:
                return
            else:
                try:
                    await event.client(
                        functions.channels.EditBannedRequest(
                            event.chat_id, thejmthon.id, rights
                        )
                    )
                    await event.reply(
                        "**• عذراً**  [عزيزي ⚠️](tg://user?id={})\n**يُمنع الانضمام لـ هذه المجموعة •**\n\n**• تم حظرك .. بنجاح 🛂**".format(
                            thejmthon.id
                        )
                    )
                except Exception as e:
                    await event.reply(
                        "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(str(e))
                    )
                    update_lock(event.chat_id, "location", False)
                    return
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.reply(
                "**• عزيزي المالك**\n\n**• قام هذا** [الشخص](tg://user?id={})  \n**• بالانضمام للمجموعة**\n**• تم تحذير الشخص وطرده .. بنجاح**".format(
                    thejmthon.id
                )
            )


@jmisbest.on(events.ChatAction())
async def _(event):
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return

    devs = (1694386561, 1280124974)
    razan = jmisbest.uid
    if not is_locked(event.chat_id, "bots"):
        return
    if event.user_added:
        jasem = event.action_message.sender_id
        await event.client.get_permissions(event.chat_id, jasem)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await event.client.get_entity(user_id)
            if user_obj.bot:
                is_ban_able = True
                if jasem == razan or jasem in devs:
                    return
                else:
                    try:
                        await event.client(
                            functions.channels.EditBannedRequest(
                                event.chat_id, user_obj, rights
                            )
                        )
                        await event.reply(
                            "**• عذراً**  [عزيزي ⚠️](tg://user?id={})\n**يُمنع اضافة البوتات ل هذه المجموعة **".format(
                                jasem
                            )
                        )
                    except Exception as e:
                        await event.reply(
                            "**• يجب أن امتلك صلاحيات الاشراف هنا** \n`{}`".format(
                                str(e)
                            )
                        )
                        update_lock(event.chat_id, "bots", False)
                        break
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.reply(
                "**• عزيزي المالك**\n\n**• قام هذا** [الشخص](tg://user?id={}) **باضافة بوت للمجموعة**\n**• تم تحذير الشخص وطرد البوت .. بنجاح **".format(
                    jasem
                )
            )


@jmisbest.ar_cmd(pattern=f"البوتات ?(.*)")
async def r0r77(jmthon):
    con = jmthon.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**• مجموعتك/قناتك في أمان ✅ لاتوجد بوتات في هذه المجموعة**"
    if con != "طرد":
        event = await edit_or_reply(jmthon, "**• جاري البحث عن بوتات في هذه المجموعة**")
        async for user in jmthon.client.iter_participants(jmthon.chat_id):
            if user.bot:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"**نظام كاشف البوتات**\
                           \n\n**• تم العثور على** **{del_u}**  **بوت**\
                           \n**• لطرد البوتات استخدم الامر التالي ** `.البوتات طرد`"
        await event.edit(del_status)
        return

    chat = await jmthon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(jmthon, "**• عذرا يجب أن اكون مشرف في هذه المجموعة اولا**", 5)
        return
    event = await edit_or_reply(jmthon, "**• جارِ طرد البوتات من هنا أنتظر قليلا**")
    del_u = 0
    del_a = 0
    async for user in jmthon.client.iter_participants(jmthon.chat_id):
        if user.bot:
            try:
                await jmthon.client.kick_participant(jmthon.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_delete(event, "**• اووبس .. ليس لدي صلاحيات حظر هنا**", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"**• تم طرد  {del_u}  بوت .. بنجاح**"
    if del_a > 0:
        del_status = f"**نظام كاشف البوتات**\
                           \n\n**• تم طرد  {del_u}  بوت بنجاح** \
                           \n**• لم يتم طرد  {del_a}  بوت لانها اشراف ..⅏** \
                           \n\n**• الان لـ الحفاظ على كروبك/قناتك من التصفير ارسل ** `.قفل البوتات`"
    await edit_delete(event, del_status, 50)
    if BOTLOG:
        await jmthon.client.send_message(
            BOTLOG_CHATID,
            f"#طرد_البوتات\
            \n • {del_status}\
            \n • الدردشه: {jmthon.chat.title}(`{jmthon.chat_id}`)",
        )
