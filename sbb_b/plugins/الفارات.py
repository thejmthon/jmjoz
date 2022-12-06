import asyncio

import urllib3

from sbb_b import sbb_b

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

# from ..Config import Config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGS = logging.getLogger(__name__)


@sbb_b.ar_cmd(pattern="اعادة تشغيل$", disable_errors=True)
async def koyeb(event):
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#اعادة_التشغيل \n" "تم اعادة تشغيل البوت"
        )
    await edit_or_reply(
        event,
        "**❃ جارِ اعادة تشغيل السورس\nارسل** `.فحص` **او** `.الاوامر` **للتحقق مما إذ كان البوت شغال ، يستغرق الأمر في الواقع 1-2 دقيقة لإعادة التشغيل**",
    )
    await event.client.reload(jmthon)


@sbb_b.ar_cmd(pattern="وضع (.*)")
async def variable(var):
    rep = await var.get_reply_message()
    vra = None
    if rep:
        vra = rep.text
    if vra is None:
        return await edit_delete(
            var, "**⌔∮ يجب عليك الرد على النص او الرابط حسب الفار الذي تضيفه **"
        )
    exe = var.pattern_match.group(1)
    await edit_or_reply(var, "**⌔∮ جارِ وضع الفار انتظر قليلا**")
    if exe == "رمز الاسم":
        await asyncio.sleep(1)
        if gvarstatus("TIME_JM") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار رمز الاسم\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار رمز الاسم \n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        addgvar("TIME_JM", vra)
    if exe == "المكرر":
        await asyncio.sleep(1)
        if gvarstatus("TKRAR") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار اسم امر مكرر\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار اسم مكرر \n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        addgvar("TKRAR", vra)
    if exe == "البايو" or exe == "النبذة":
        await asyncio.sleep(1)
        if gvarstatus("DEFAULT_BIO") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كليشة الفحص\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كليشة الفحص\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        addgvar("DEFAULT_BIO", vra)
    if exe == "الصورة" or exe == "الصوره":
        await asyncio.sleep(1)
        if gvarstatus("DIGITAL_PIC") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار صورة الحساب\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار صورة الحساب\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        addgvar("DIGITAL_PIC", vra)
    if exe == "اسم" or exe == "الاسم":
        await asyncio.sleep(1)
        if gvarstatus("ALIVE_NAME") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار اسم المستخدم\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار اسم المستخدم\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        addgvar("DIGITAL_PIC", vra)
    if exe == "كليشة الفحص" or exe == "كليشه الفحص":
        await asyncio.sleep(1)
        if gvarstatus("ALIVE_TEMPLATE") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كليشة الفحص\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كليشة الفحص\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        addgvar("ALIVE_TEMPLATE", vra)
    if (
        exe == "كليشة الحماية"
        or exe == "كليشة الحمايه"
        or exe == "كليشه الحماية"
        or exe == "كليشه الحمايه"
    ):
        await asyncio.sleep(1)
        if gvarstatus("pmpermit_txt") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كليشة الحماية\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كليشة الحماية\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        addgvar("pmpermit_txt", vra)
    if exe == "كليشة الحظر" or exe == "كليشه الحظر":
        await asyncio.sleep(1)
        if gvarstatus("pmblock") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كليشة الحظر\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كليشة الحظر\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        addgvar("pmblock", vra)
    if exe == "ايموجي الفحص":
        await asyncio.sleep(1)
        if gvarstatus("ALIVE_EMOJI") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار ايموجي الفحص\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار ايموجي الفحص\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        addgvar("ALIVE_EMOJI", vra)
    if exe == "نص الفحص":
        await asyncio.sleep(1)
        if gvarstatus("ALIVE_TEXT") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار نص الفحص\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار نص الفحص\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        addgvar("ALIVE_TEXT", vra)
    if exe == "عدد التحذيرات":
        await asyncio.sleep(1)
        if gvarstatus("MAX_FLOOD_IN_PMS") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار عدد التحذيرات\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار عدد التحذيرات\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        addgvar("MAX_FLOOD_IN_PMS", vra)
    if (
        exe == "صورة الحماية"
        or exe == "صورة الحمايه"
        or exe == "صوره الحماية"
        or exe == "صوره الحمايه"
    ):
        await asyncio.sleep(1)
        if gvarstatus("pmpermit_pic") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار صورة الحماية\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار صورة الحماية\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        addgvar("pmpermit_pic", vra)
    if exe == "صورة الفحص" or exe == "صوره الفحص":
        await asyncio.sleep(1)
        if gvarstatus("ALIVE_PIC") is None:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار صورة الحماية\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار صورة الحماية\n\n❃ جار اعادة تشغيل السورس انتظر دقيقة ليتشغل مره اخرى**",
            )
        addgvar("ALIVE_PIC", vra)
