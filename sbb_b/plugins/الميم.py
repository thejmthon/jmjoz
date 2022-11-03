import asyncio

from sbb_b import sbb_b

from ..core.managers import edit_or_reply


@sbb_b.ar_cmd(pattern="فصخ ([\s\S]*)")
async def typewriter(typew):
    message = typew.pattern_match.group(1)
    sleep_time = 0.2
    typing_symbol = "|"
    old_text = ""
    typew = await edit_or_reply(typew, typing_symbol)
    await asyncio.sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await asyncio.sleep(sleep_time)
        await typew.edit(old_text)
        await asyncio.sleep(sleep_time)


@sbb_b.ar_cmd(pattern="عيد (\d*) ([\s\S]*)")
async def _(event):
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    count = int(cat[0])
    repsmessage = (f"{message}") * count
    await edit_or_reply(event, repsmessage)
