# =============================
# |         sbb_b - QHR_1 - RR7PP           |
# =============================

import os

from telegraph import exceptions, upload_file

from sbb_b import sbb_b

from ..core.managers import edit_or_reply
from ..helpers.utils import _jmthonutils, reply_id
from . import convert_toimage, deEmojify, phcomment, threats, trap, trash


@sbb_b.ar_cmd(pattern="تراش$")
async def catbot(event):
    replied = await event.get_reply_message()
    rozid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "⌯︙قم بالرد على احد الصور")
    output = await _jmthonutils.media_to_pic(event, replied)
    if output[1] is None:
        return await edit_delete(
            output[0], "⌯︙عدم الاستطاعة على الاستخراج من الرد الحالي"
        )
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    if size > 5242880:
        os.remove(download_location)
        return await output[0].edit(
            "⌯︙الصورة/الملصق المردود عليه يجب يكون اقل من 5 ميغابايت"
        )
    await event.reply(file=download_location)
    await output[0].edit("⌯︙جار الصنع..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await output[0].edit(f"**⌔︙خطأ: **\n`{str(exc)}`")
    sbb_b = f"https://telegra.ph{response[0]}"
    sbb_b = await trash(sbb_b)
    os.remove(download_location)
    await output[0].delete()
    await event.client.send_file(event.chat_id, sbb_b, reply_to=rozid)


@sbb_b.ar_cmd(pattern="تهديد$")
async def catbot(event):
    replied = await event.get_reply_message()
    catid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "⌯︙قم بالرد على احد الصور")
    output = await _jmthonutils.media_to_pic(event, replied)
    if output[1] is None:
        return await edit_delete(
            output[0], "⌯︙عدم الاستطاعة على الاستخراج من الرد الحالي"
        )
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    if size > 5242880:
        os.remove(download_location)
        return await output[0].edit(
            "⌯︙الصورة/الملصق المردود عليه يجب يكون اقل من 5 ميغابايت"
        )
    await output[0].edit("⌯︙جار الصنع..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await output[0].edit(f"**⌯︙خطأ: **\n`{str(exc)}`")
    cat = f"https://telegra.ph{response[0]}"
    cat = await threats(cat)
    await output[0].delete()
    os.remove(download_location)
    await event.client.send_file(event.chat_id, cat, reply_to=catid)


@sbb_b.ar_cmd(pattern="فخ(?:\s|$)([\s\S]*)")
async def catbot(event):
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        text1, text2 = input_str.split(";")
    else:
        return await edit_or_reply(
            event,
            "⌔︙** يجـب الـرد على صورة او ملصق بـ**\n `.فخ (إسم الضحية);(إسم الفاعل)`",
        )
    replied = await event.get_reply_message()
    catid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "⌯︙قم بالرد على احد الصور")
    output = await _jmthonutils.media_to_pic(event, replied)
    if output[1] is None:
        return await edit_delete(
            output[0], "⌯︙عدم الاستطاعة على الاستخراج من الرد الحالي"
        )
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    if size > 5242880:
        os.remove(download_location)
        return await output[0].edit(
            "⌯︙ الصورة/الملصق المردود عليه يجب يكون اقل من 5 ميغابايت "
        )
    await output[0].edit("⌔︙جار الصنع..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await output[0].edit(f"**⌔︙خطأ: **\n`{str(exc)}`")
    cat = f"https://telegra.ph{response[0]}"
    cat = await trap(text1, text2, cat)
    await output[0].delete()
    os.remove(download_location)
    await event.client.send_file(event.chat_id, cat, reply_to=catid)


@sbb_b.ar_cmd(pattern="بورن(?:\s|$)([\s\S]*)")
async def catbot(event):
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        username, text = input_str.split(";")
    else:
        return await edit_or_reply(
            event,
            "**⌯︙يجـب الـرد على صورة/ملصق بـ\n `.بورن (المعرف);(النص)`",
        )
    replied = await event.get_reply_message()
    catid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "⌯︙قم بالرد على احد الصور")
    output = await _jmthonutils.media_to_pic(event, replied)
    if output[1] is None:
        return await edit_delete(
            output[0], "⌯︙عدم الاستطاعة على الاستخراج من الرد الحالي"
        )
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    if size > 5242880:
        os.remove(download_location)
        return await output[0].edit(
            "⌯︙الصورة/الملصق المردود عليه يجـب يكون اقل من 5 ميغابايت "
        )

    await output[0].edit("⌯︙جار الصنع..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await output[0].edit(f"**⌔︙خطأ: **\n`{str(exc)}`")
    cat = f"https://telegra.ph{response[0]}"
    cat = await phcomment(cat, text, username)
    await output[0].delete()
    os.remove(download_location)
    await event.client.send_file(event.chat_id, cat, reply_to=catid)
