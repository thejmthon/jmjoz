import io
import sys
import traceback

from ..helpers.utils import _format
from . import *


@jmisbest.ar_cmd(pattern="امر التجربة")
async def hi(event):
    await edit_or_reply(
        event,
        "**[ . ᯏ𝖩𝗆𝗍𝗁𝗈ꪀ - ᥴ𝗆𝖽 ᭡ .](t.me/jmthon)\n✦┅━╍━╍╍━━╍━━╍━┅✦**\n\n الامر: `.تجربة` + كود برمجي\n- يقوم بتشغيل الكود و أظهار النتيجة",
        link_preview=False,
    )


@jmisbest.ar_cmd(pattern="تجربة(?:\s|$)([\s\S]*)")
async def _(event):
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await edit_delete(event, "**- يجب عليك كتابة الكود مع الامر اولا**")
    cmd = (
        cmd.replace("sendmessage", "send_message")
        .replace("sendfile", "send_file")
        .replace("editmessage", "edit_message")
    )
    jmthon = await edit_or_reply(event, "**- جار التشغيل أنتظر قليلا**")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = (
        f"**•  الكود : **\n```{cmd}``` \n\n**•  النتيجة : **\n```{evaluation}``` \n"
    )
    await edit_or_reply(
        jmthon,
        text=final_output,
        aslink=True,
        linktext=f"**•  الكود : **\n```{cmd}``` \n\n**•  النتيجة : **\n",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"**- تم بنجاح تشغيل وتجربة امر {cmd}**."
        )


async def aexec(code, smessatatus):
    message = event = smessatatus
    p = lambda _x: print(_format.yaml_format(_x))
    reply = await event.get_reply_message()
    exec(
        (
            "async def __aexec(message, event , reply, client, p, chat): "
            + "".join(f"\n {l}" for l in code.split("\n"))
        )
    )

    return await locals()["__aexec"](
        message, event, reply, message.client, p, message.chat_id
    )
