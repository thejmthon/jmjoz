import os
import shutil

from telethon.errors.rpcerrorlist import MediaEmptyError

from jmrobot import jmrobot

from ..core.managers import edit_or_reply
from ..helpers.google_image_download import googleimagesdownload
from ..helpers.utils import reply_id


@jmrobot.ar_cmd(pattern="صور(?: |$)(\d*)? ?([\s\S]*)")
async def img_sampler(event):
    reply_to_id = await reply_id(event)
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await edit_or_reply(
            event, "⌔∮ يجب عليك كتابه ما تريد البحث عنه مع الامر"
        )
    jmrobot = await edit_or_reply(event, "**❃ يتم البحث انتظر قليلا**")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim > 10:
            lim = int(10)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(3)
    response = googleimagesdownload()
    arguments = {
        "keywords": query.replace(",", " "),
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }
    try:
        paths = response.download(arguments)
    except Exception as e:
        return await jmrobot.edit(f"Error: \n`{e}`")
    lst = paths[0][query.replace(",", " ")]
    try:
        await event.client.send_file(event.chat_id, lst, reply_to=reply_to_id)
    except MediaEmptyError:
        for i in lst:
            try:
                await event.client.send_file(event.chat_id, i, reply_to=reply_to_id)
            except MediaEmptyError:
                pass
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await jmrobot.delete()
