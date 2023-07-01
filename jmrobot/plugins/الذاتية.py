from telethon import events

from jmrobot import jmrobot

from ..sql_helper.globals import addgvar, delgvar, gvarstatus

# ها ولك جاي تخمط خرب عقلك اي والله 😂🏃


@jmrobot.ar_cmd(pattern="تفعيل الذاتية")
async def start_datea(event):
    if gvarstatus("DATEA"):
        return await edit_or_reply(event, "حفظ الذاتية مفعل بالأًصل")
    else:
        await edit_or_reply(event, "- تم بنجاح تفعيل حفظ الميديا الذاتية من الان")
        addgvar("DATEA", "True")


@jmrobot.ar_cmd(pattern="تعطيل الذاتية")
async def stop_datea(event):
    if gvarstatus("DATEA"):
        delgvar("DATEA")
        return await edit_or_reply(
            event, "- تم بنجاح تعطيل حفظ الميديا الذاتية من الان"
        )
    else:
        await edit_or_reply(event, "حفظ الذاتية غير مفعل بالأًصل")


@jmrobot.on(
    events.NewMessage(
        func=lambda e: e.is_private and (e.photo or e.video) and e.media_unread
    )
)
async def tf3el(event):
    if gvarstatus("DATEA"):
        sender = await event.get_sender()
        username = sender.username
        user_id = sender.id

        result = await event.download_media()
        caption = (
            f"ميديا ذاتية التدمير وصلت لك !\n: المرسل @{username}\nالايدي : {user_id}"
        )
        await jmrobot.send_file("me", result, caption=caption)
