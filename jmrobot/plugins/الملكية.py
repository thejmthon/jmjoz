import telethon.password as pwd_mod
from telethon.tl import functions

from jmrobot import jmrobot

from ..Config import Config


@jmrobot.ar_cmd(pattern="تحويل ملكية ([\s\S]*)")
async def _(event):
    user_name = event.pattern_match.group(1)
    try:
        pwd = await event.client(functions.account.GetPasswordRequest())
        my_srp_password = pwd_mod.compute_check(pwd, Config.TG_2STEP_VERIFICATION_CODE)
        await event.client(
            functions.channels.EditCreatorRequest(
                channel=event.chat_id, user_id=user_name, password=my_srp_password
            )
        )
    except Exception as e:
        await event.edit(f"**خطأ:**\n`{e}`")
    else:
        await event.edit("**- تم نقل الملكية  بنجاح**")
