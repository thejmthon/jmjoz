import asyncio

from telethon import events
from telethon.tl.functions.contacts import GetBlockedRequest, UnblockRequest

from jmisbest import jmisbest

loop = asyncio.get_event_loop()


async def unblock_users(jmisbest):
    @jmisbest.on(events.NewMessage(outgoing=True, pattern=".فك المحظورين"))
    async def _(event):
        list = await jmisbest(GetBlockedRequest(offset=0, limit=1000000))
        if len(list.blocked) == 0:
            razan = await event.edit(f"- لم تقم بحظر اي شخص اصلا .")
        else:
            unblocked_count = 1
            for user in list.blocked:
                UnBlock = await jmisbest(UnblockRequest(id=int(user.peer_id.user_id)))
                unblocked_count += 1
                razan = await event.edit(
                    f"- جار الغاء حظر  {round((unblocked_count * 100) / len(list.blocked), 2)}%"
                )
            unblocked_count = 1
            razan = await event.edit(
                f"- تم الغاء حظر : {len(list.blocked)}\n\n- تم المستخدمين المحظورين في الخاص بنجاح  ."
            )


loop.create_task(unblock_users(jmisbest))
