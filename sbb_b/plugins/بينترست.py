import re

from razan.strings import get_download_url
from sbb_b import sbb_b


@sbb_b.ar_cmd(pattern="بينترست?(.*)")
async def _(event):
    R = event.pattern_match.group(1)
    links = re.findall(r"\bhttps?://.*\.\S+", R)
    await event.delete()
    if not links:
        Z = await event.respond("▾∮ يجب عليك وضع رابط لتحميله")
        await asyncio.sleep(2)
        await Z.delete()
    else:
        pass
    A = await event.respond("▾∮ يتم التحميل انتظر قليلا")
    RR7PP = get_download_url(R)
    await event.client.send_file(event.chat.id, RR7PP)
    await A.delete()
