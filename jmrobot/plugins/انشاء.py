from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from jmrobot import jmrobot


@jmrobot.ar_cmd(pattern="انشاء ?(.*)")
async def handle_creation_command(event):
    msg = event.text.split()
    username = msg[1]
    chat = "@creationdatebot"
    response = await jmrobot.send_message("creationdatebot", f"/id {username}")
    async with event.client.conversation(chat) as conv:
        try:
            await event.client.send_message(chat, "/id {reply_message}")
        except YouBlockedUserError:
            await event.reply(
                f"يجب عليك الغاء حظر هذا البوت @creationdatebot اولا واعادة استخدام الامر"
            )
            return
        response = conv.wait_event(
            events.NewMessage(incoming=True, from_users=747653812)
        )
        response = await response
        if response.text.startswith("Looks"):
            await event.edit("لقد حدث خطأ ما")
        else:
            await event.edit(
                f"**تاريخ انشاء المستخدم هو: **`{response.text.replace('**','')}`"
            )
