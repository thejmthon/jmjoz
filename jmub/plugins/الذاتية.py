from os import remove

from jmub import jmub


@jmub.ar_cmd(pattern="(سي|ذاتية)")
async def datea(event):
    await event.delete()
    scertpic = await event.get_reply_message()
    downloadjmthon = await scertpic.download_media()
    await jmub.send_file("me", downloadjmthon)
    remove(downloadjmthon)
