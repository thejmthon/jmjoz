from telethon import events

from jmub import jmub

# ها ولك جاي تخمط خرب عقلك اي والله 😂🏃

jmthonself = False


@jmub.ar_cmd(pattern="تفعيل الحفظ")
async def start_datea(event):
    global jmthonself
    jmthonself = True
    await edit_or_reply(event, "- تم بنجاح تفعيل حفظ الميديا الذاتية من الان")


@jmub.ar_cmd(pattern="تعطيل الحفظ")
async def stop_datea(event):
    global jmthonself
    jmthonself = False
    await edit_or_reply(event, "- تم بنجاح تعطيل حفظ الميديا الذاتية من الان")


@jmub.on(
    events.NewMessage(
        func=lambda e: e.is_private and (e.photo or e.video) and e.media_unread
    )
)
async def tf3el(event):
    global jmthonself
    if jmthonself:
        sender = await event.get_sender()
        username = sender.username
        user_id = sender.id

        result = await event.download_media()
        caption = (
            f"ميديا ذاتية التدمير وصلت لك !\n: المرسل @{username}\nالايدي : {user_id}"
        )
        await jmub.send_file("me", result, caption=caption)
