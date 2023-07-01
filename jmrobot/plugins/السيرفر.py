import asyncio
import glob
import os
import re

from validators.url import url

from jmrobot import jmrobot

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _jmthonutils

config = "./config.py"
var_checker = [
    "APP_ID",
    "PM_LOGGER_GROUP_ID",
    "PRIVATE_CHANNEL_BOT_API_ID",
    "PRIVATE_GROUP_BOT_API_ID",
    "PLUGIN_CHANNEL",
]
exts = ["jpg", "png", "webp", "webm", "m4a", "mp4", "mp3", "tgs"]

cmds = [
    "rm -rf downloads",
    "mkdir downloads",
]


async def switch_branch():
    with open(config, "r") as f:
        configs = f.read()
    BRANCH = "master"
    REPO = "https://github.com/thejmthon/jmrobot0"
    EXTERNAL = False
    for match in re.finditer(
        r"(?:(UPSTREAM_REPO|UPSTREAM_REPO_BRANCH|EXTERNAL_REPO)(?:[ = \"\']+(.*[^\"\'\n])))",
        configs,
    ):
        BRANCH = match.group(2) if match.group(1) == "UPSTREAM_REPO_BRANCH" else BRANCH
        REPO = match.group(2) if match.group(1) == "UPSTREAM_REPO" else REPO
        EXTERNAL = match.group(2) if match.group(1) == "EXTERNAL_REPO" else EXTERNAL
    if REPO:
        await _jmthonutils.runcmd(f"git clone -b {BRANCH} {REPO} TempJmthon")
        file_list = os.listdir("TempJmthon")
        for file in file_list:
            await _jmthonutils.runcmd(f"rm -rf {file}")
            await _jmthonutils.runcmd(f"mv ./TempJmthon/{file} ./")
        await _jmthonutils.runcmd("pip3 install --no-cache-dir -r requirements.txt")
        await _jmthonutils.runcmd("rm -rf TempJmthon")
    if not EXTERNAL and os.path.exists("xtraplugins"):
        await _jmthonutils.runcmd("rm -rf xtraplugins")


@jmrobot.ar_cmd(pattern="(وضع|جلب|حذف) فار ([\s\S]*)")
async def variable(event):  # sourcery no-metrics
    if not os.path.exists(config):
        return await edit_delete(
            event, "**- لم يتم العثور على ملف الفارات لم يتم تشغيل هذا الأمر**"
        )
    cmd = event.pattern_match.group(1)
    string = ""
    match = None
    with open(config, "r") as f:
        configs = f.readlines()
    if cmd == "جلب":
        jmthon = await edit_or_reply(event, "- جار جلب قيمة هذا الفار")
        await asyncio.sleep(1)
        variable = event.pattern_match.group(2).split()[0]
        for i in configs:
            if variable in i:
                _, val = i.split("= ")
                return await edit_or_reply(
                    jmthon, "**معلومات الفار**:" f"\n\n`{variable}` = `{val}`"
                )
        await edit_or_reply(
            jmthon,
            "**معلومات الفار***:" f"\n\nخطأ:\nالمتغير `{variable}` لم استطع ايجاده",
        )
    elif cmd == "وضع":
        variable = "".join(event.text.split(maxsplit=2)[2:])
        jmthon = await edit_or_reply(event, "**- جار وضع قيمة هذا الفار**")
        if not variable:
            return await jmthon.edit("`.وضع فار <الفار/المتغير> <قيمة الفار>`")
        value = "".join(variable.split(maxsplit=1)[1:])
        variable = "".join(variable.split(maxsplit=1)[0])
        if not value:
            return await edit_or_reply(
                jmthon, "`.وضع فار <الفار/المتغير> <قيمة الفار>`"
            )
        if variable not in var_checker:
            if variable == "EXTERNAL_REPO":
                if bool(value and (value.lower() != "false")) and not url(value):
                    value = "https://github.com/thejmthon/Plugins"
                else:
                    return await edit_or_reply(
                        jmthon,
                        f"**لا يوجد اي فائدة من وضع الفار `{variable}` مع القيمة: `{value}`\nارسل`.حذف فار <الفار/المتغير>` لحذفه**",
                    )
            value = f"'{value}'"
        await asyncio.sleep(1)
        for i in configs:
            if variable in i:
                string += f"    {variable} = {value}\n"
                match = True
            else:
                string += f"{i}"
        if match:
            await edit_or_reply(
                jmthon,
                f"المتغير: `{variable}`\n**تم بنجاح تغيير قيمة الفار الى:**\n`{value}`",
            )
        else:
            string += f"    {variable} = {value}\n"
            await edit_or_reply(
                jmthon,
                f"المتغير: `{variable}`\n**تم بنجاح تغيير قيمة الفار الى:**\n`{value}`",
            )
        with open(config, "w") as f1:
            f1.write(string)
            f1.close()
        await switch_branch()
        await event.client.reload(jmthon)
    if cmd == "حذف":
        jmthon = await edit_or_reply(event, "**- جار حذف قيممة هذا الفار**")
        await asyncio.sleep(1)
        variable = event.pattern_match.group(2).split()[0]
        for i in configs:
            if variable in i:
                match = True
            else:
                string += f"{i}"
        with open(config, "w") as f1:
            f1.write(string)
            f1.close()
        if not match:
            return await edit_or_reply(
                jmthon,
                "**معلومات الفارات**:" f"\n\nخطأ:\nالمتغير {variable}` لم يتم ايجاده",
            )
        await edit_or_reply(jmthon, f"المتغير`{variable}`\n**تم بنجاح حذف قيمته.**")
        await switch_branch()
        await event.client.reload(jmthon)


@jmrobot.ar_cmd(pattern="(ري|كلين)لود$")
async def _(event):
    cmd = event.pattern_match.group(1)
    jmthon = await edit_or_reply(
        event, "**- الان أنتظر من 2-3 دقائق ليتم تشغيل السورس**"
    )
    if cmd == "clean":
        for file in exts:
            removing = glob.glob(f"./*.{file}")
            for i in removing:
                os.remove(i)
        for i in cmds:
            await _jmthonutils.runcmd(i)
    await switch_branch()
    await event.client.reload(jmthon)
