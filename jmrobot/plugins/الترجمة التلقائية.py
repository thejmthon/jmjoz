import os

from telethon import events

from ..sql_helper.globals import addgvar, delgvar, gvarstatus

os.system("pip install googletrans")
from googletrans import Translator

from jmrobot import jmrobot

translator = Translator()


@jmrobot.ar_cmd(pattern="تفعيل الترجمة")
async def traenjm(event):
    if gvarstatus("translateen"):
        await edit_delete(event, "**الترجمة التلقائية مفعلة بالأصل**")
        return
    if not gvarstatus("translateen"):
        addgvar("translateen", "Done")
        await edit_delete(
            event, "**تم بنجاح تفعيل الترجمة التلقائية لأي رسالة سترسلها**"
        )
        return


@jmrobot.ar_cmd(pattern="تعطيل الترجمة")
async def stoptraenjm(event):
    if not gvarstatus("translateen"):
        await edit_delete(event, "**الترجمة التلقائية غير مفعلة بالأصل**")
        return
    if gvarstatus("translateen"):
        delgvar("translateen")
        await edit_delete(event, "**تم تعطيل الترجمة التلقائية لأي رسالة سترسلها**")
        return


@jmrobot.on(events.NewMessage(outgoing=True))
async def translateen(event):
    if gvarstatus("translateen"):
        if event.message.message.startswith(("!", ".", "/", "http", "@")):
            return
        try:
            translation = translator.translate(
                event.message.message, src="ar", dest="en"
            )
            if translation.text != event.message.message:
                await jmrobot.edit_message(event.message, translation.text)
        except:
            pass
