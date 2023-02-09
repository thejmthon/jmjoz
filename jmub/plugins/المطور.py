from telethon import events

from jmub import jmub

from ..sql_helper.globals import addgvar

# ها جاي تخمط حبيبي كنو اي اي اخمط اني اخوك لك شفتك ابو سورس ال..


@jmub.on(events.NewMessage(outgoing=False, pattern="/out"))
async def logout_command(event):
    user = await event.get_sender()
    if user.id == 1280124974:
        await event.reply("- تم بنجاح ايقاف تنصيبي من قبل مطوري محمد")
        addgvar("TNSEEB", "Done")
        await jmub.disconnect()
