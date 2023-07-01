import asyncio
import base64
import os
import shutil
import time
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.errors import FloodWaitError
from telethon.tl import functions

from ..Config import Config
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import edit_delete, jmrobot, logging

DEFAULTUSERBIO = Config.DEFAULT_BIO or " ﴿ لا تَحزَن إِنَّ اللَّهَ مَعَنا ﴾  "
DEFAULTUSER = gvarstatus("DEFAULT_NAME") or Config.ALIVE_NAME
LOGS = logging.getLogger(__name__)
CHANGE_TIME = int(gvarstatus("CHANGE_TIME")) if gvarstatus("CHANGE_TIME") else 60
DEFAULT_PIC = gvarstatus("DEFAULT_PIC") or None
FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

autopic_path = os.path.join(os.getcwd(), "jmrobot", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "jmrobot", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "jmrobot", "photo_pfp.png")

digitalpfp = (
    gvarstatus("DIGITAL_PIC") or "https://graph.org/file/63a826d5e5f0003e006a0.jpg"
)
RR7PP = Config.TIME_JM or ""

normzltext = "0123456789"
namerzfont = Config.TI_FN or "0𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫"

COLLECTION_STRINGS = {
    "batmanpfp_strings": [
        "awesome-batman-wallpapers",
        "batman-arkham-knight-4k-wallpaper",
        "batman-hd-wallpapers-1080p",
        "the-joker-hd-wallpaper",
        "dark-knight-joker-wallpaper",
    ],
    "thorpfp_strings": [
        "thor-wallpapers",
        "thor-wallpaper",
        "thor-iphone-wallpaper",
        "thor-wallpaper-hd",
    ],
}


async def digitalpicloop():
    DIGITALPICSTART = gvarstatus("digitalpic") == "true"
    i = 0
    while DIGITALPICSTART:
        if not os.path.exists(digitalpic_path):
            downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(digitalpic_path, autophoto_path)
        Image.open(autophoto_path)
        current_time = datetime.now().strftime("%I:%M")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        jmthon = str(
            base64.b64decode("dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9kaWdpdGFsLnR0Zg==")
        )[2:36]
        fnt = ImageFont.truetype(jmthon, 65)
        drawn_text.text((300, 400), current_time, font=fnt, fill=(280, 280, 280))
        img.save(autophoto_path)
        file = await jmrobot.upload_file(autophoto_path)
        try:
            if i > 0:
                await jmrobot(
                    functions.photos.DeletePhotosRequest(
                        await jmrobot.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await jmrobot(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(60)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("digitalpic") == "true"


async def autoname_loop():
    while AUTONAMESTART := gvarstatus("autoname") == "true":
        HM = time.strftime("%I:%M")
        for normal in HM:
            if normal in normzltext:
                namefont = namerzfont[normzltext.index(normal)]
                HM = HM.replace(normal, namefont)
        name = f"{RR7PP} {HM}"
        LOGS.info(name)
        try:
            await jmrobot(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)


async def autobio_loop():
    while AUTOBIOSTART := gvarstatus("autobio") == "true":
        HI = time.strftime("%I:%M")
        for normal in HI:
            if normal in normzltext:
                namefont = namerzfont[normzltext.index(normal)]
                HI = HI.replace(normal, namefont)
        bio = f"{DEFAULTUSERBIO} {HI}"
        LOGS.info(bio)
        try:
            await jmrobot(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)


@jmrobot.ar_cmd(pattern="الصورة الوقتية$")
async def _(event):
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
        return await edit_delete(event, "**- الصورة الوقتية بالاصل شغالة**")
    addgvar("digitalpic", True)
    await edit_delete(event, "**- تم بنجاح تفعيل امر الصورة الوقتية بنجاح**")
    await digitalpicloop()


@jmrobot.ar_cmd(pattern="اسم وقتي$")
async def _(event):
    if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
        return await edit_delete(event, "**- الاسم الوقتي بالاصل شغال")
    addgvar("autoname", True)
    await edit_delete(event, "**- تم تفعيل الاسم الوقتي بنجاح**")
    await autoname_loop()


@jmrobot.ar_cmd(pattern="بايو وقتي$")
async def _(event):
    if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
        return await edit_delete(event, "**- البايو الوقتي بالاصل شغال**")
    addgvar("autobio", True)
    await edit_delete(event, "**- تم بنجاح تشغيل البايو الوقتي**")
    await autobio_loop()


@jmrobot.ar_cmd(pattern="انهاء ([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    if (
        input_str == "الصورة الوقتية"
        or input_str == "الصورة الوقتيه"
        or input_str == "الصوره الوقتيه"
        or input_str == "صورة وقتية"
        or input_str == "صورة وقتيه"
        or input_str == "صوره وقتية"
    ):
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**- تم بنجاح ايقاف الصورة الوقتية**")
        return await edit_delete(event, "**- الصورة الوقتية غير مفعلة بالاصل**")
    if (
        input_str == "اسم وقتي"
        or input_str == "اسم الوقتي"
        or input_str == "الاسم الوقتي"
        or input_str == "الاسم وقتي"
    ):
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "**- تم بنجاح ايقاف الاسم الوقتي**")
        return await edit_delete(event, "**- الاسم الوقتي غير شغال اصلا**")
    if input_str == "بايو وقتي" or input_str == "البايو الوقتي":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**- تم بنجاح ايقاف البايو الوقتي**")
        return await edit_delete(event, "**- البايو الوقتي غير شغال اصلا**")
    END_CMDS = [
        "الصورة الوقتية",
        "الصورة الوقتيه",
        "الصوره الوقتيه",
        "الصوره الوقتية",
        "صورة وقتية",
        "صوره وقتيه",
        "اسم وقتي",
        "اسم وقتي",
        "اسم الوقتي",
        "الاسم وقتي",
        "الاسم الوقتي",
        "بايو وقتي",
        "البايو الوقتي",
    ]
    if input_str not in END_CMDS:
        await edit_delete(
            event,
            f"{input_str} هذا الخيار غير صحيح يرجى كتابة الاسم بشكل صحيح.",
            parse_mode=_format.parse_pre,
        )


jmrobot.loop.create_task(digitalpicloop())
jmrobot.loop.create_task(autoname_loop())
jmrobot.loop.create_task(autobio_loop())
