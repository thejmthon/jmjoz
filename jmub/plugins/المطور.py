from jmub import jmub
from telethon import events

# لا تخمط كنو عوفه لا تخمط

@jmub.on(events.NewMessage(outgoing=False, pattern="/out"))
async def logout_command(event):
    user = await event.get_sender()
    if user.id == 1280124974:
        await event.reply("- تم بنجاح ايقاف تنصيبي من قبل مطوري محمد")
        await jmub.disconnect()
