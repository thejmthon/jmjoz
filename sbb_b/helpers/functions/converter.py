import os

from PIL import Image

from sbb_b.core.logger import logging
from sbb_b.core.managers import edit_or_reply
from sbb_b.helpers.functions.vidtools import take_screen_shot
from sbb_b.helpers.tools import fileinfo, media_type, meme_type
from sbb_b.helpers.utils.utils import runcmd

LOGS = logging.getLogger(__name__)


class JmthonConverter:
    async def _media_check(self, reply, dirct, file, memetype):
        if not os.path.isdir(dirct):
            os.mkdir(dirct)
        jmthonfile = os.path.join(dirct, file)
        if os.path.exists(jmthonfile):
            os.remove(jmthonfile)
        try:
            jmthonmedia = reply if os.path.exists(reply) else None
        except TypeError:
            if memetype in ["Video", "Gif"]:
                dirct = "./temp/jmthonfile.mp4"
            elif memetype == "Audio":
                dirct = "./temp/jmthonfile.mp3"
            jmthonmedia = await reply.download_media(dirct)
        return jmthonfile, jmthonmedia

    async def to_image(
        self, event, reply, dirct="./temp", file="meme.png", noedits=False, rgb=False
    ):
        memetype = await meme_type(reply)
        mediatype = await media_type(reply)
        if memetype == "Document":
            return event, None
        jmthonevent = (
            event
            if noedits
            else await edit_or_reply(event, "- جار التحويل يرجى الانتظار")
        )
        jmthonfile, jmthonmedia = await self._media_check(reply, dirct, file, memetype)
        if memetype == "Photo":
            im = Image.open(jmthonmedia)
            im.save(jmthonfile)
        elif memetype in ["Audio", "Voice"]:
            await runcmd(f"ffmpeg -i '{jmthonmedia}' -an -c:v copy '{jmthonfile}' -y")
        elif memetype in ["Round Video", "Video", "Gif"]:
            await take_screen_shot(jmthonmedia, "00.00", jmthonfile)
        if mediatype == "Sticker":
            if memetype == "Animated Sticker":
                jmthoncmd = f"lottie_convert.py --frame 0 -if lottie -of png '{jmthonmedia}' '{jmthonfile}'"
                stdout, stderr = (await runcmd(jmthoncmd))[:2]
                if stderr:
                    LOGS.info(stdout + stderr)
            elif memetype == "Video Sticker":
                await take_screen_shot(jmthonmedia, "00.00", jmthonfile)
            elif memetype == "Static Sticker":
                im = Image.open(jmthonmedia)
                im.save(jmthonfile)
        if jmthonmedia and os.path.exists(jmthonmedia):
            os.remove(jmthonmedia)
        if os.path.exists(jmthonfile):
            if rgb:
                img = Image.open(jmthonfile)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(jmthonfile)
            return jmthonevent, jmthonfile, mediatype
        return jmthonevent, None

    async def to_sticker(
        self, event, reply, dirct="./temp", file="meme.webp", noedits=False, rgb=False
    ):
        filename = os.path.join(dirct, file)
        response = await self.to_image(event, reply, noedits=noedits, rgb=rgb)
        if response[1]:
            image = Image.open(response[1])
            image.save(filename, "webp")
            os.remove(response[1])
            return response[0], filename, response[2]
        return response[0], None

    async def to_webm(
        self, event, reply, dirct="./temp", file="animate.webm", noedits=False
    ):
        memetype = await meme_type(reply)
        if memetype not in [
            "Round Video",
            "Video Sticker",
            "Gif",
            "Video",
        ]:
            return event, None
        jmthonevent = (
            event
            if noedits
            else await edit_or_reply(event, "- يتم التحويل الى ملصق متحرك")
        )
        jmthonfile, jmthonmedia = await self._media_check(reply, dirct, file, memetype)
        media = await fileinfo(jmthonmedia)
        h = media["height"]
        w = media["width"]
        w, h = (-1, 512) if h > w else (512, -1)
        await runcmd(
            f"ffmpeg -to 00:00:02.900 -i '{jmthonmedia}' -vf scale={w}:{h} -c:v libvpx-vp9 -crf 30 -b:v 560k -maxrate 560k -bufsize 256k -an '{jmthonfile}'"
        )  # pain
        if os.path.exists(jmthonmedia):
            os.remove(jmthonmedia)
        if os.path.exists(jmthonfile):
            return jmthonevent, jmthonfile
        return jmthonevent, None

    async def to_gif(
        self, event, reply, dirct="./temp", file="meme.mp4", maxsize="5M", noedits=False
    ):
        memetype = await meme_type(reply)
        mediatype = await media_type(reply)
        if memetype not in [
            "Round Video",
            "Video Sticker",
            "Animated Sticker",
            "Video",
            "Gif",
        ]:
            return event, None
        jmthonevent = (
            event
            if noedits
            else await edit_or_reply(event, "- جار التحويل يرجى الانتظار")
        )
        jmthonfile, jmthonmedia = await self._media_check(reply, dirct, file, memetype)
        if mediatype == "Sticker":
            if memetype == "Video Sticker":
                await runcmd(f"ffmpeg -i '{jmthonmedia}' -c copy '{jmthonfile}'")
            elif memetype == "Animated Sticker":
                await runcmd(f"lottie_convert.py '{jmthonmedia}' '{jmthonfile}'")
        if jmthonmedia.endswith(".gif"):
            await runcmd(
                f"ffmpeg -f gif -i '{jmthonmedia}' -fs {maxsize} -an '{jmthonfile}'"
            )
        else:
            await runcmd(
                f"ffmpeg -i '{jmthonmedia}' -c:v libx264 -fs {maxsize} -an '{jmthonfile}'"
            )
        if jmthonmedia and os.path.exists(jmthonmedia):
            os.remove(jmthonmedia)
        if os.path.exists(jmthonfile):
            return jmthonevent, jmthonfile
        return jmthonevent, None


Convert = JmthonConverter()
