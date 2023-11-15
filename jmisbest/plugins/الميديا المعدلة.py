from telethon import events

from jmisbest import jmisbest

from ..utils import is_admin


@jmisbest.ar_cmd(pattern="تعطيل تعديل الميديا")
async def cleanup_command(event):
    if await is_admin(event.client, event.chat_id, event.sender_id):
        global handler

        @jmisbest.on(events.MessageEdited(incoming=True, chats=event.chat_id))
        async def handler(event):
            if event.media:
                await event.client.delete_messages(event.chat_id, event.id)

        await event.edit("- تم تفعيل نظام حذف الميديا المعدلة")
    else:
        await event.edit("- ليس لديك الصلاحيات الكافية لأستخدام هذا الامر.")


@jmisbest.ar_cmd(pattern="فتح تعديل الميديا")
async def stop_cleanup_command(event):
    if await is_admin(event.client, event.chat_id, event.sender_id):
        jmisbest.remove_event_handler(handler)
        await event.edit("- تم تعطيل نظام حذف الميديا المعدلة.")
    else:
        await event.edit("- ليس لديك الصلاحيات الكافية لأستخدام هذا الامر.")
