from telethon import events

from jmrobot import jmrobot

from ..sql_helper.globals import addgvar, delgvar, gvarstatus


@jmrobot.ar_cmd(pattern="تفعيل الزخرفة الانجليزية")
async def zakrafaon(event):
    if not gvarstatus("enzakrafa"):
        addgvar("enzakrafa", "on")
        await edit_delete(event, "**تم بنجاح تفعيل الزخرفة الانجليزية**")
        return
    if gvarstatus("enzakrafa"):
        await edit_delete(event, "**الزخرفة الانجليزية مفعلة اصلا**")
        return


@jmrobot.ar_cmd(pattern="تعطيل الزخرفة الانجليزية")
async def zakrafaoff(event):
    if not gvarstatus("enzakrafa"):
        await edit_delete(event, "*الزخرفة الانجليزية غير مفعلة اصلا**")
        return
    if gvarstatus("enzakrafa"):
        delgvar("enzakrafa")
        await edit_delete(event, "**تم بنجاح تعطيل الزخرفة الانجليزية**")
        return


@jmrobot.on(events.NewMessage(outgoing=True))
async def zakrafarun(event):
    if gvarstatus("enzakrafa"):
        text = event.message.message
        uppercase_text = (
            text.replace("a", "𝗮")
            .replace("b", "𝗯")
            .replace("c", "𝗰")
            .replace("d", "𝗱")
            .replace("e", "𝗲")
            .replace("f", "𝗳")
            .replace("g", "𝗴")
            .replace("h", "𝗵")
            .replace("i", "𝗶")
            .replace("j", "𝗷")
            .replace("k", "𝗸")
            .replace("l", "𝗹")
            .replace("m", "𝗺")
            .replace("n", "𝗻")
            .replace("o", "𝗼")
            .replace("p", "𝗽")
            .replace("q", "𝗾")
            .replace("r", "𝗿")
            .replace("s", "𝘀")
            .replace("t", "𝘁")
            .replace("u", "𝘂")
            .replace("v", "𝘃")
            .replace("w", "𝘄")
            .replace("x", "𝘅")
            .replace("y", "𝘆")
            .replace("z", "𝘇")
        )
        await event.edit(uppercase_text)
