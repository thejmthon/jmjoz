from os import remove
from telethon import events 
import asyncio
from jmub import jmub

jmthonself = False


@jmub.ar_cmd(pattern="(سي|ذاتية)")
async def datea(event):
    await event.delete()
    scertpic = await event.get_reply_message()
    downloadjmthon = await scertpic.download_media()
    await jmub.send_file("me", downloadjmthon)
    remove(downloadjmthon)


@jmub.ar_cmd(pattern="تفعيل الذاتية")
async def start_downloader():
    global jmthonself
    jmthonself = True
    await event.edit("- تم بنجاح تفعيل حفظ الميديا الذاتية من الان")

@jmub.ar_cmd(pattern="تعطيل الذاتية")
async def stop_downloader():
    global jmthonself
    jmthonself = False
    await event.edit("- تم بنجاح تعطيل حفظ الميديا الذاتية من الان")

@jmub.on(events.NewMessage(func=lambda e: e.is_private and (e.photo or e.video) and e.media_unread))
async def downloader(event):
    global jmthonself
    if jmthonself:
        result = await event.download_media()
        await jmub.send_file("me", result, caption="- تم بنجاح الحفظ بواسطة @jmthon")
