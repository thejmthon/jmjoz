import re

from telethon.utils import get_display_name

from sbb_b import sbb_b

from ..core.managers import edit_or_reply
from ..sql_helper.filter_sql import (
    add_filter,
    get_filters,
    remove_all_filters,
    remove_filter,
)
from . import BOTLOG, BOTLOG_CHATID


@sbb_b.ar_cmd(incoming=True)
async def filter_incoming_handler(event):
    if event.sender_id == event.client.uid:
        return
    name = event.raw_text
    filters = get_filters(event.chat_id)
    if not filters:
        return
    a_user = await event.get_sender()
    chat = await event.get_chat()
    me = await event.client.get_me()
    title = get_display_name(await event.get_chat()) or "هذه الدردشة"
    participants = await event.client.get_participants(chat)
    count = len(participants)
    mention = f"[{a_user.first_name}](tg://user?id={a_user.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = a_user.first_name
    last = a_user.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{a_user.username}" if a_user.username else mention
    userid = a_user.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    for trigger in filters:
        pattern = f"( |^|[^\\w]){re.escape(trigger.keyword)}( |$|[^\\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            file_media = None
            filter_msg = None
            if trigger.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                )
                file_media = msg_o.media
                filter_msg = msg_o.message
                link_preview = True
            elif trigger.reply:
                filter_msg = trigger.reply
                link_preview = False
            await event.reply(
                filter_msg.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
                link_preview=link_preview,
            )


@sbb_b.ar_cmd(pattern="رد (.*)")
async def add_new_filter(event):
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"اضافة رد\
            \nايدي المجموعة: {event.chat_id}\
            \nالرد: {keyword}\
            \n\nالرسالة التالية تم حفظها على شكل يرجى عدم حذفها نهائيا",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                event,
                "**- اذا كنت تريد حفظ الميديا على شكل رد عليك وضع فارات التخزين والحفظ اولا**",
            )
            return
    elif msg and msg.text and not string:
        string = msg.text
    elif not string:
        return await edit_or_reply(event, "- يجب استخدام الامر بشكل صحيح")
    success = "الرد **{}** تم {} بنجاح"
    if add_filter(str(event.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(event, success.format(keyword, "حفظه"))
    remove_filter(str(event.chat_id), keyword)
    if add_filter(str(event.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(event, success.format(keyword, "تحديثه"))
    await edit_or_reply(event, f"لقد حدث اثناء اعداد الرد {keyword}")


@sbb_b.ar_cmd(pattern="الردود$")
async def on_snip_list(event):
    OUT_STR = "**- لم يتم حفظ اي رد هنا**"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if OUT_STR == "- لا يوجد اي رد تم حفظه هنا.":
            OUT_STR = "ردود المجموعة الحالية هي:\n"
        OUT_STR += "- `{}`\n".format(filt.keyword)
    await edit_or_reply(
        event,
        OUT_STR,
        caption="- لا يوجد اي رد تم حفظه هنا.",
        file_name="الردود.text",
    )


@sbb_b.ar_cmd(pattern="حذف رد ([\s\S]*)")
async def remove_a_filter(event):
    filt = event.pattern_match.group(1)
    if not remove_filter(event.chat_id, filt):
        await event.edit(f"الرد {filt} لا يوجد اصلا")
    else:
        await event.edit(f"الرد {filt} تم بنجاح حذفه")


@sbb_b.ar_cmd(
    pattern="حذف الردود$",
)
async def on_all_snip_delete(event):
    if filters := get_filters(event.chat_id):
        remove_all_filters(event.chat_id)
        await edit_or_reply(event, "**- تم بنجاح حذف جميع الردود**")
    else:
        await edit_or_reply(event, "**- لا  توجد اي ردود هنا لحذفها**")
