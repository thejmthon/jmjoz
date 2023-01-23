# by: t.me/Dar4k

import random
import asyncio
import telethon
from telethon import events
import requests
from telethon.sync import functions
from user_agent import generate_user_agent
import requests
from user_agent import *
from sbb_b import sbb_b

a = 'qwertyuiopassdfghjklzxcvbnm'
b = '1234567890'
e = 'qwertyuiopassdfghjklzxcvbnm1234567890'

trys, trys2 = [0], [0]
isclaim = ["off"]
isauto = ["off"]


def check_user(username):
    url = "https://t.me/"+str(username)
    headers = {
        "User-Agent": generate_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7"}

    response = requests.get(url, headers=headers)
    if response.text.find('If you have <strong>Telegram</strong>, you can contact <a class="tgme_username_link"') >= 0:
        return "Available"
    else:
        with open("users.txt", "a") as f:
            f.write(f"\n{username}")
        return "Unavailable"


def gen_user(choice):
    if choice == "سداسي حرفين":
        c = d = random.choices(a)
        d = random.choices(b)
        f = [c[0], d[0], c[0], c[0], c[0], d[0]]
        random.shuffle(f)
        username = ''.join(f)

    elif choice == "ثلاثيات":
        c = random.choices(a)
        d = random.choices(b)
        s = random.choices(e)
        f = [c[0], "_", d[0], "_", s[0]]
        username = ''.join(f)
    elif choice == "سداسيات":
        c = d = random.choices(a)
        d = random.choices(e)
        f = [c[0], c[0], c[0], c[0], c[0], d[0]]
        random.shuffle(f)
        username = ''.join(f)
    elif choice == "بوتات":
        c = random.choices(a)
        d = random.choices(e)
        s = random.choices(e)
        f = [c[0], s[0], d[0]]
        # random.shuffle(f)
        username = ''.join(f)
        username = username+'bot'

    elif choice == "خماسي حرفين":
        c = random.choices(a)
        d = random.choices(e)

        f = [c[0], d[0], c[0], c[0], d[0]]
        random.shuffle(f)
        username = ''.join(f)

    elif choice == "خماسي":
        c = d = random.choices(a)
        d = random.choices(b)
        f = [c[0], c[0], c[0], c[0], d[0]]
        random.shuffle(f)
        username = ''.join(f)

    elif choice == "سباعيات":
        c = d = random.choices(a)
        d = random.choices(b)
        f = [c[0], c[0], c[0], c[0], d[0], c[0], c[0]]
        random.shuffle(f)
        username = ''.join(f)
    elif choice == "تيست":
        c = d = random.choices(a)
        d = random.choices(b)
        f = [c[0], d[0], c[0], d[0], d[0], c[0], c[0], d[0], c[0], d[0]]
        random.shuffle(f)
        username = ''.join(f)
    else:
        return "error"
    return username


@sbb_b.on(events.NewMessage(outgoing=True, pattern=r"\.الصيد"))
async def _(event):
    await event.edit('''
.صيد + النوع  + القناة يلي تريد تثبت عليها (اختياري)
الانواع : ثلاثيات - بوتات - سباعيات - خماسي - سداسيات
مثال : .صيد ثلاثيات @jmthon

.تثبيت + اليوزر الي تريد تثبت عليه + القناة يلي تريد تثبت عليها (اختياري)
مثال : .تثبيت dar4k

`.حالة الصيد` | لعرض حالة الصيد
`.حالة التثبيت` | لعرض حالة التثبيت
''')


# كلايم عدد نوع قناة


@sbb_b.on(events.NewMessage(outgoing=True, pattern=r"\.صيد (.*)"))
async def _(event):
    msg = event.text.split()
    choice = str(msg[1])
    try:

        ch = str(msg[2])
        if '@' in ch:
            ch = ch.replace("@", "")
        await event.edit(f"حسناً سيتم بدء الصيد في @{ch} .")
    except:
        try:
            ch = await sbb_b(functions.channels.CreateChannelRequest(
                title='jmthon check',
                about='Best src in the whole world ! - @jmthon ',
            ))
            ch = ch.updates[1].channel_id
            await event.edit(f"حسناً سيتم بدء الصيد !")
            pass
        except Exception as e:
            await sbb_b.send_message(event.chat_id, f"خطأ في انشاء القناة , الخطأ : {str(e)}")
    isclaim.clear()
    isclaim.append("on")
    for i in range(19000000):
        username = gen_user(choice)
        if username == "error":
            return
        isav = check_user(username)
        if "Available" in isav:
            await asyncio.sleep(1)
            try:
                await sbb_b(functions.channels.UpdateUsernameRequest(
                    channel=ch, username=username))
                await event.client.send_message(event.chat_id, f'''
    تم صيد (@{username}) !
    جمثون : @jmthon
    محمد : @R0R77
    ''')
                break
            except telethon.errors.rpcerrorlist.UsernameInvalidError:
                pass
            except telethon.errors.FloodError as e:
                await sbb_b.send_message(event.chat_id, f"للاسف تبندت , مدة الباند ({e.seconds}) ثانية .")
                break
            except Exception as eee:
                if "The username is already" in str(eee):
                  pass
                else :
                  await sbb_b.send_message(event.chat_id, f'''خطأ مع @{username} , الخطأ :
{str(eee)}''')
                  break
        else:
            pass
        trys[0] += 1
    isclaim.clear()
    isclaim.append("off")
    await event.client.send_message(event.chat_id, "تم الانتهاء من الصيد")


@sbb_b.on(events.NewMessage(outgoing=True, pattern=r"\.تثبيت (.*)"))
async def _(event):
    trys = 0
    msg = event.text.split()
    try:
        ch = str(msg[2])
        await event.edit(f"حسناً سيتم بدء التثبيت في @{ch} .")
    except:
        try:
            ch = await sbb_b(functions.channels.CreateChannelRequest(
                title='jmthon Check',
                about='Best src in the whole world ! - @jmthon ',
            ))
            ch = ch.updates[1].channel_id
            await event.edit(f"حسناً سيتم بدء التثبيت !")
            pass
        except Exception as e:
            await sbb_b.send_message(event.chat_id, f"خطأ في انشاء القناة , الخطأ : {str(e)}")
    isauto.clear()
    isauto.append("on")
    username = str(msg[1])

    for i in range(1000000000000):
        isav = check_user(username)
        if "Available" in isav:
            try:
                await sbb_b(functions.channels.UpdateUsernameRequest(
                    channel=ch, username=username))
                await event.client.send_message(event.chat_id, f'''
    تم صيد (@{username}) !
    جمثون : @jmthon
    محمد : @R0R77
    ''')
                break
            except telethon.errors.rpcerrorlist.UsernameInvalidError:
                await event.client.send_message(event.chat_id, f"اليوزر @{username} مبند . ")
                break
            except telethon.errors.FloodError as e:
                await sbb_b.send_message(event.chat_id, f"للاسف تبندت , مدة الباند ({e.seconds}) ثانية .")
                break
            except Exception as eee:
                await sbb_b.send_message(event.chat_id, f'''خطأ مع {username} , الخطأ :
{str(eee)}''')
        else:
            pass
        trys2[0] += 1

        await asyncio.sleep(5)
    trys = ""
    isclaim.clear()
    isclaim.append("off")
    await sbb_b.send_message(event.chat_id, "تم الانتهاء من التثبيت ")


@sbb_b.on(events.NewMessage(outgoing=True, pattern=r"\.حالة الصيد"))
async def _(event):
    if "on" in isclaim:
        await event.edit(f"الصيد وصل لـ({trys[0]}) من المحاولات")
    elif "off" in isclaim:
        await event.edit("الصيد لايعمل .")
    else:
        await event.edit("خطأ")


@sbb_b.on(events.NewMessage(outgoing=True, pattern=r"\.حالة التثبيت"))
async def _(event):
    if "on" in isauto:
        await event.edit(f"التثبيت وصل لـ({trys2[0]}) من المحاولات")
    elif "off" in isauto:
        await event.edit("التثبيت لايعمل .")
    else:
        await event.edit("خطأ")
