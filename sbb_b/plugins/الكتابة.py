from sbb_b import sbb_b


@sbb_b.ar_cmd(pattern="تغميق(?: |$)(.*)")
async def _(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.text
        event.reply_to_msg_id
        the_real_message = the_real_message.replace("*", "*")
        the_real_message = the_real_message.replace("_", "_")
        await event.edit(f"**{the_real_message}**")
    else:
        await event.edit("**⌔∮ يجب عليك الرد على الرساله**")


@sbb_b.ar_cmd(pattern="نسخ(?: |$)(.*)")
async def _(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.text
        event.reply_to_msg_id
        the_real_message = the_real_message.replace("*", "*")
        the_real_message = the_real_message.replace("_", "_")
        await event.edit(f"`{the_real_message}`")
    else:
        await event.edit("**⌔∮ يجب عليك الرد على الرساله**")


@sbb_b.ar_cmd(pattern="مائل(?: |$)(.*)")
async def _(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.text
        event.reply_to_msg_id
        the_real_message = the_real_message.replace("*", "*")
        the_real_message = the_real_message.replace("_", "_")
        await event.edit(f"__{the_real_message}__")
    else:
        await event.edit("**⌔∮ يجب عليك الرد على الرساله**")
