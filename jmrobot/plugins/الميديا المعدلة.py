from telethon import events

from jmrobot import jmrobot

from ..utils import is_admin


@jmrobot.ar_cmd(pattern="تعطيل تعديل الميديا")
async def cleanup_command(event):
    if await is_admin(event.client, event.chat_id, event.sender_id):
        global handler

        @jmrobot.on(events.MessageEdited(incoming=True, chats=event.chat_id))
        async def handler(event):
            if event.media:
                await event.client.delete_messages(event.chat_id, event.id)

        await event.edit("- تم تفعيل نظام حذف الميديا المعدلة")
    else:
        await event.edit("- ليس لديك الصلاحيات الكافية لأستخدام هذا الامر.")


@jmrobot.ar_cmd(pattern="فتح تعديل الميديا")
async def stop_cleanup_command(event):
    if await is_admin(event.client, event.chat_id, event.sender_id):
        jmrobot.remove_event_handler(handler)
        await event.edit("- تم تعطيل نظام حذف الميديا المعدلة.")
    else:
        await event.edit("- ليس لديك الصلاحيات الكافية لأستخدام هذا الامر.")
