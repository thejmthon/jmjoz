from telethon.errors.rpcerrorlist import YouBlockedUserError

from jmrobot import jmrobot

from . import *


@jmrobot.ar_cmd(pattern="حفظ كتابة$")
async def save(e):
    razan = await e.get_reply_message()
    if not razan:
        return await edit_delete(
            e, "- يجب عليك اولا الرد على الرسالة لحفظها في الرسائل المحفوظة", time=8
        )
    if e.out:
        await e.client.send_message("me", razan)
    else:
        await e.client.send_message(e.sender_id, razan)
    await edit_delete(e, "- تم بنجاح حفظ الرسالة في الرسائل المحفوظة", time=8)


@jmrobot.ar_cmd(pattern="حفظ توجيه$")
async def saf(e):
    razan = await e.get_reply_message()
    if not razan:
        return await edit_delete(
            e, "- يجب عليك اولا الرد على الرسالة لحفظها في الرسائل المحفوظة", time=8
        )
    if e.out:
        await razan.forward_to("me")
    else:
        await razan.forward_to(e.sender_id)
    await edit_delete(e, "- تم بنجاح حفظ الرسالة في الرسائل المحفوظة", time=8)


@jmrobot.ar_cmd(pattern="همسة ?(.*)")
async def roz(event):
    razan = event.pattern_match.group(1)
    BE = "@whisperBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    R7 = await jmrobot.inline_query(BE, razan)
    await R7[0].click(event.chat_id)
    await event.delete()


@jmrobot.ar_cmd(pattern="ايجاد الفايروسات$")
async def _(event):
    input_str = event.pattern_match.group(1)
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "**- يجب عليك الرد على رسالة المستخدم**")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "**- يجب عليك الرد عل ميديا اولا**")
        return
    chat = "@VS_Robot"
    jmthonevent = await edit_or_reply(event, "**- انتظر قليلا الان من فضلك**")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await event.client.forward_messages(chat, reply_message)
            response1 = await conv.get_response()
            if response1.text:
                await event.client.send_read_acknowledge(conv.chat_id)
                return await jmthonevent.edit(response1.text, parse_mode=parse_pre)
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            response3 = await conv.get_response()
            response4 = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await jmthonevent.edit(
                "**- يجب عليك الغاء حظر بوت @VS_Robot و المحاولة مرة اخرى**"
            )
        if not input_str:
            await edit_or_reply(jmthonevent, response4.text)
            await jmthonevent.delete()
            await event.client.send_file(
                event.chat_id, response3.media, reply_to=(await reply_id(event))
            )
