# t.me/Dar4k
# this file for https://github.com/thejmthon/jmub0
import asyncio

from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest

from jmub import jmub


@jmub.ar_cmd(pattern="تجميع$")
async def _(event):
    await event.edit("حسنا, تأكد من انك مشترك ب قنوات الاشتراك الاجباري لتجنب الأخطأء")
    channel_entity = await jmub.get_entity("@t06bot")
    await jmub.send_message("@t06bot", "/start")
    await asyncio.sleep(5)
    msg0 = await jmub.get_messages("@t06bot", limit=1)
    await msg0[0].click(2)
    await asyncio.sleep(5)
    msg1 = await jmub.get_messages("@t06bot", limit=1)
    await msg1[0].click(0)

    chs = 1
    for i in range(100):
        await asyncio.sleep(5)
        list = await jmub(
            GetHistoryRequest(
                peer=channel_entity,
                limit=1,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0,
            )
        )
        msgs = list.messages[0]
        if (
            msgs.message.find(
                "لا يوجد قنوات في الوقت الحالي , قم يتجميع النقاط بطريقه مختلفه"
            )
            != -1
        ):
            await jmub.send_message(
                event.chat_id, f"**- لا توجد قنوات متاحة في البوت**"
            )
            break
        url = msgs.reply_markup.rows[0].buttons[0].url
        try:
            try:
                await jmub(JoinChannelRequest(url))
            except:
                bott = url.split("/")[-1]
                await jmub(ImportChatInviteRequest(bott))
            msg2 = await jmub.get_messages("@t06bot", limit=1)
            await msg2[0].click(text="تحقق")
            chs += 1
            await event.edit("- تم بنجاح الاشتراك في {chs} قناة")
        except FloodWaitError as e:
            await event.edit(
                f"خطأ لقد تحصلت على فلود ويت بمقدار: {e}. ثواني سيكمل التجميع بعد انتهاء الوقت."
            )
            sleep_time = int(str(e).split("in ")[1].split(" seconds")[0])
            await asyncio.sleep(sleep_time)


# t.me/r0r77
@jmub.ar_cmd(pattern="بخشيش وعد (.*)")
async def baqshis(event):
    for i in range(int("".join(event.text.split(maxsplit=2)[2:]).split(" ", 2)[0])):
        chat = event.chat_id
        await jmub.send_message(chat, "بخشيش")
        await asyncio.sleep(605)


@jmub.ar_cmd(pattern="راتب وعد (.*)")
async def ratb(event):
    for i in range(int("".join(event.text.split(maxsplit=2)[2:]).split(" ", 2)[0])):
        chat = event.chat_id
        await jmub.send_message(chat, "راتب")
        await asyncio.sleep(605)


# none
@jmub.ar_cmd(pattern="كلمات وعد (.*)")
async def waorwaad(event):
    for i in range(int("".join(event.text.split(maxsplit=2)[2:]).split(" ", 2)[0])):
        chat = event.chat_id
        await jmub.send_message(chat, "كلمات")
        await asyncio.sleep(0.5)
        masg = await jmub.get_messages(chat, limit=1)
        masg = masg[0].message
        masg = ("".join(masg.split(maxsplit=3)[3:])).split(" ", 2)
        if len(masg) == 2:
            msg = masg[0]
            await jmub.send_message(chat, msg)
        else:
            msg = masg[0] + " " + masg[1]
            await jmub.send_message(chat, msg)


@jmub.ar_cmd(pattern="استثمار وعد (.*)")
async def _(event):
    await event.edit(
        "**- تم تفعيل الاستثمار ببوت وعد بنجاح لأيقافه ارسل \n`.استثمار وعد 1`"
    )
    for i in range(int("".join(event.text.split(maxsplit=2)[2:]).split(" ", 2)[0])):
        chat = event.chat_id
        await jmub.send_message(chat, "فلوسي")
        await asyncio.sleep(0.5)
        masg = await jmub.get_messages(chat, limit=1)
        masg = masg[0].message
        masg = ("".join(masg.split(maxsplit=2)[2:])).split(" ", 2)
        msg = masg[0]
        if int(msg) > 500000000:
            await jmub.send_message(chat, f"استثمار {msg}")
            await asyncio.sleep(10)
            mssag2 = await jmub.get_messages(chat, limit=1)
            await mssag2[0].click(text="اي ✅")
        else:
            await jmub.send_message(chat, f"استثمار {msg}")
        await asyncio.sleep(1210)
