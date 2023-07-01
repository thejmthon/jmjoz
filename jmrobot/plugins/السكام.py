import asyncio

from jmrobot import jmrobot


@jmrobot.ar_cmd(pattern="وهمي كتابه(?: |$)(.*)")
async def _(event):
    roz = event.pattern_match.group(1)
    if not (roz or roz.isdigit()):
        roz = 100
    else:
        try:
            roz = int(roz)
        except BaseException:
            try:
                roz = await event.ban_time(roz)
            except BaseException:
                return await event.edit("**- عليك كتابة الامر بشكل صحيح**")
    await event.edit(f"**- تم بدء وضع الكتابه الوهمي ل {roz} من الثوانـي**")
    async with event.client.action(event.chat_id, "typing"):
        await asyncio.sleep(roz)


@jmrobot.ar_cmd(pattern="وهمي صوت(?: |$)(.*)")
async def _(event):
    roz = event.pattern_match.group(1)
    if not (roz or roz.isdigit()):
        roz = 100
    else:
        try:
            roz = int(roz)
        except BaseException:
            try:
                roz = await event.ban_time(roz)
            except BaseException:
                return await event.edit("**- عليك كتابة الامر بشكل صحيح**")
    await event.edit(f"**- تم بدء وضع ارسال تسجيل الصوت الوهمي ل {roz} من الثوانـي**")
    async with event.client.action(event.chat_id, "record-audio"):
        await asyncio.sleep(roz)


@jmrobot.ar_cmd(pattern="وهمي فيديو(?: |$)(.*)")
async def _(event):
    roz = event.pattern_match.group(1)
    if not (roz or roz.isdigit()):
        roz = 100
    else:
        try:
            roz = int(roz)
        except BaseException:
            try:
                roz = await event.ban_time(roz)
            except BaseException:
                return await event.edit("**- عليك كتابة الامر بشكل صحيح**")
    await event.edit(f"**- تم بدء وضع ارسال الفيديو الوهمي ل {roz} من الثوانـي**")
    async with event.client.action(event.chat_id, "record-video"):
        await asyncio.sleep(roz)


@jmrobot.ar_cmd(pattern="وهمي لعبه(?: |$)(.*)")
async def _(event):
    roz = event.pattern_match.group(1)
    if not (roz or roz.isdigit()):
        roz = 100
    else:
        try:
            roz = int(roz)
        except BaseException:
            try:
                roz = await event.ban_time(roz)
            except BaseException:
                return await event.edit("**- عليك كتابة الامر بشكل صحيح**")
    await event.edit(f"**- تم بدء وضع اللعب الوهمي ل {roz} من الثوانـي**")
    async with event.client.action(event.chat_id, "game"):
        await asyncio.sleep(roz)
