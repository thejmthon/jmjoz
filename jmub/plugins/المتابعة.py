from jmub import jmub
from jmub.sql_helper.MOrakb import *

from ..Config import Config


@jmub.ar_cmd(incoming=True, func=lambda e: e.is_group, edited=False, forword=None)
async def forward_to_saved_messages(event):
    if event.is_private:
        return
    if event.sender_id == event.chat_id:
        return
    if event.is_group:
        if is_morakb(event.sender_id) and not event.forward:
            await event.client.forward_messages(
                Config.PM_LOGGER_GROUP_ID, event.message
            )


@jmub.ar_cmd(pattern=r"متابعة")
async def add_morakb_handler(event):
    msg = event.text.split()
    username = msg[1]
    user = await jmub.get_entity(username)
    replied_user = user.id
    if is_morakb(replied_user):
        await event.reply("هذا المستخدم في قائمة المتابعة في الاصل.")
    else:
        addmorakb(replied_user)
        await event.reply("تم بنجاح اضافة المستخدمالى قائمة المتابعة بنجاح.")


@jmub.ar_cmd(pattern=r"الغاء متابعة")
async def remove_morakb_handler(event):
    msg = event.text.split()
    username = msg[2]
    user = await jmub.get_entity(username)
    replied_user = user.id
    if not is_morakb(replied_user):
        await event.reply("هذا المستخدم ليس في قائمة المتابعة في الاصل.")
    else:
        unmorakb(replied_user)
        await event.reply("تم بنجاح الغاء متابعة المستخدم.")
