from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from ..utils import is_admin
from jmub import jmub 

@jmub.ar_cmd(pattern='تعطيل تعديل الميديا')
async def cleanup_command(event):
    if await is_admin(event.client, event.chat_id, event.sender_id):
        global handler
        @jmub.on(events.MessageEdited(incoming=True, chats=event.chat_id))
        async def handler(event):
            if event.media:
                await event.client.delete_messages(event.chat_id, event.id)
        await event.edit("- تم تفعيل نظام حذف الميديا المعدلة")
    else:
        await event.edit("- ليس لديك الصلاحيات الكافية لأستخدام هذا الامر.")

@jmub.ar_cmd(pattern='فتح تعديل الميديا')
async def stop_cleanup_command(event):
    if await is_admin(event.client, event.chat_id, event.sender_id):
        jmub.remove_event_handler(handler)
        await event.edit("- تم تعطيل نظام حذف الميديا المعدلة.")
    else:
        await event.edit("- ليس لديك الصلاحيات الكافية لأستخدام هذا الامر.")
