from ..helpers.functions.functions import make_inline
from . import edit_delete, jmrobot, reply_id


@jmrobot.ar_cmd(pattern="لستة(?:\s|$)([\s\S]*)")
async def _(event):
    reply_to_id = await reply_id(event)
    reply_message = await event.get_reply_message()
    if reply_message:
        markdown_note = reply_message.text
    else:
        markdown_note = "".join(event.text.split(maxsplit=1)[1:])
    if not markdown_note:
        return await edit_delete(event, "**- يجب عليك كتابة الامر بشكل صحيح**")
    await make_inline(markdown_note, event.client, event.chat_id, reply_to_id)
    await event.delete()
