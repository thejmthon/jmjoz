from os import remove

from jmthon import jmthon


@jmthon.ar_cmd(pattern="(سي|ذاتية)")
async def datea(event):
    await event.delete()
    scertpic = await event.get_reply_message()
    downloadjmthon = await scertpic.download_media()
    await jmthon.send_file("me", downloadjmthon)
    remove(downloadjmthon)
