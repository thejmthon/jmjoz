from telethon import functions
from telethon.sync import errors

from jmrobot import jmrobot


@jmrobot.ar_cmd(pattern="كروباتي$")
async def oeo(event):
    result = await jmrobot(functions.channels.GetGroupsForDiscussionRequest())
    alist = []
    for item in result.chats:
        username = (
            "  | @" + item.username
            if hasattr(item, "username") and item.username
            else " "
        )
        roz = str(item.id) + " | " + item.title + username
        print(roz)
        alist.append(roz)
    if alist:
        await jmrobot.send_message("me", "\n".join(alist))


@jmrobot.ar_cmd(pattern="الحاظرهم$")
async def main(event):
    result = await jmrobot(
        functions.contacts.GetBlockedRequest(offset=0, limit=1000000)
    )
    alist = []
    for user in result.users:
        if not user.bot:
            username = "@" + user.username if user.username else " "
            roz = f"{user.id} {user.first_name} {username}"
            print(roz)
            alist.append(roz)
    if alist:
        await jmrobot.send_message("me", "\n".join(alist))


@jmrobot.ar_cmd(pattern="قيد (.*)")
async def se(event):
    exe = event.text[5:]
    try:
        result = await jmrobot(
            functions.messages.ToggleNoForwardsRequest(peer=exe, enabled=True)
        )
        await event.edit("تم بنجاح تفعيل وضع تقييد المحتوى")
    except errors.ChatNotModifiedError as e:
        print(e)  # خاف ما تغير شي يعني القناة اصلا مفعل بيهل تقييد محتوى


@jmrobot.ar_cmd(pattern="نوعه (.*)")
async def se(event):
    exe = event.text[5:]
    x = await jmrobot.get_entity(exe)
    if hasattr(x, "megagroup") and x.megagroup:
        await event.edit("نوع المعرف : كروب")
    elif hasattr(x, "megagroup") and not x.megagroup:
        await event.edit("نوع المعرف : قناة")
    elif hasattr(x, "bot") and x.bot:
        await event.edit("نوع المعرف : بوت")
    else:
        await event.edit("نوع المعرف : لحساب")


@jmrobot.ar_cmd(pattern="احذف (.*)")
async def se(event):
    exe = event.text[5:]
    await jmrobot.get_dialogs()
    chat = exe
    await jmrobot.delete_dialog(chat, revoke=True)
    await event.edit("- تم بنجاح حذف الدردشة مع المستخدم بنجاح")
