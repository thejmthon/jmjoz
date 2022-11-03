import os

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl import functions
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User

from sbb_b import sbb_b

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply

LOGS = logging.getLogger(__name__)


INVALID_MEDIA = "⌔∮ امتداد الصورة غير صالح."
PP_CHANGED = "⌔∮ تم تغيير صورة الملف الشخصي بنجاح."
PP_TOO_SMOL = "⌔∮ هذه الصورة صغيرة جدًا ، استخدم صورة أكبر."
PP_ERROR = "⌔∮ حدث فشل أثناء معالجة الصورة."
BIO_SUCCESS = "⌔∮ تم تغيير البايو بنجاح."
NAME_OK = "⌔∮ تم تغيير اسمك بنجاح."
USERNAME_SUCCESS = "⌔∮ تم تغيير اسم المستخدم الخاص بك بنجاح."
USERNAME_TAKEN = "⌔∮ أسم المستخدم مأخوذ مسبقا."


@sbb_b.ar_cmd(pattern="وضع بايو ([\s\S]*)")
async def _(event):
    bio = event.pattern_match.group(1)
    try:
        await event.client(functions.account.UpdateProfileRequest(about=bio))
        await edit_delete(event, "**- تم بنجاح تغيير البايو او النبذة**")
    except Exception as e:
        await edit_or_reply(event, f"**خطأ:**\n`{e}`")


@sbb_b.ar_cmd(pattern="وضع اسم ([\s\S]*)")
async def _(event):
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if ";" in names:
        first_name, last_name = names.split(";", 1)
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await edit_delete(event, "**- تم بنجاح تغيير الاسم**")
    except Exception as e:
        await edit_or_reply(event, f"**خطأ:**\n`{e}`")


@sbb_b.ar_cmd(pattern="وضع صورة$")
async def _(event):
    reply_message = await event.get_reply_message()
    jmthonevent = await edit_or_reply(
        event, "**- جار تحميل الصورة الى قاعدة البيانات انتظر قليلا**"
    )
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await event.client.download_media(
            reply_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e:
        await jmthonevent.edit(str(e))
    else:
        if photo:
            await jmthonevent.edit("**- جار الرفع على اتلجرام انتظر قليلا**")
            if photo.endswith((".mp4", ".MP4")):
                size = os.stat(photo).st_size
                if size > 2097152:
                    await jmthonevent.edit("**- يجب ان يكون الحجم اقل من 2 ميغا**")
                    os.remove(photo)
                    return
                jmthonpic = None
                jmthonvideo = await event.client.upload_file(photo)
            else:
                jmthonpic = await event.client.upload_file(photo)
                jmthonvideo = None
            try:
                await event.client(
                    functions.photos.UploadProfilePhotoRequest(
                        file=jmthonpic, video=jmthonvideo, video_start_ts=0.01
                    )
                )
            except Exception as e:
                await jmthonevent.edit(f"**خطا:**\n`{e}`")
            else:
                await edit_or_reply(jmthonevent, "**- تم بنجاح تحديث صورة الحساب**")
    try:
        os.remove(photo)
    except Exception as e:
        LOGS.info(str(e))


@sbb_b.ar_cmd(pattern="وضع يوزر ([\s\S]*)")
async def update_username(event):
    newusername = event.pattern_match.group(1)
    try:
        await event.client(UpdateUsernameRequest(newusername))
        await edit_delete(event, USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await edit_or_reply(event, USERNAME_TAKEN)
    except Exception as e:
        await edit_or_reply(event, f"**خطا:**\n`{e}`")


@sbb_b.ar_cmd(pattern="حسابي$")
async def count(event):
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    jmthonevent = await edit_or_reply(event, "**- جار التعداد انتظر قليلا**")
    dialogs = await event.client.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            LOGS.info(d)

    result += f"المعرف:\t**{u}**\n"
    result += f"الكروب:\t**{g}**\n"
    result += f"المجموعة الخارقة:\t**{c}**\n"
    result += f"القنوات:\t**{bc}**\n"
    result += f"البوتات:\t**{b}**"

    await jmthonevent.edit(result)


@sbb_b.ar_cmd(pattern="ازالة الصورة ?([\s\S]*)")
async def remove_profilepic(delpfp):
    group = delpfp.text[8:]
    if group == "جميعها":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.sender_id, offset=0, max_id=0, limit=lim)
    )
    input_photos = [
        InputPhoto(
            id=sep.id,
            access_hash=sep.access_hash,
            file_reference=sep.file_reference,
        )
        for sep in pfplist.photos
    ]
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await edit_delete(delpfp, f"**- تم بنجاح حذف {len(input_photos)} من صور الحساب")


@sbb_b.ar_cmd(pattern="معرفاتي$")
async def _(event):
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "**المعرفات الخاصه بك التي تم صنعها:**\n" + "".join(
        f" - {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )
    await edit_or_reply(event, output_str)
