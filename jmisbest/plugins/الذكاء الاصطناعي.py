from somnium import Somnium

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import GetStylesGraph, reply_id
from ..sql_helper.globals import addgvar, gvarstatus
from . import jmisbest


@jmisbest.ar_cmd(
    pattern="صورة(?:\s|$)([\s\S]*)",
)
async def ai_img(odi):
    reply_to_id = await reply_id(odi)
    query = odi.pattern_match.group(1)
    if not query:
        return await edit_delete(odi, "**- يجب عليك تحديد عنوان للصورة اولا**")

    moevent = await edit_or_reply(odi, "**- جار الان الصنع يرجى الانتظار قليلا**")
    rstyles = {value: key for key, value in Somnium.Styles().items()}
    styleid = int(gvarstatus("DREAM_STYLE") or "84")

    if query.startswith("النوع"):
        query = query.replace("النوع", "").strip()
        if query.isnumeric():
            if int(query) in rstyles:
                addgvar("DREAM_STYLE", int(query))
                return await edit_delete(
                    moevent, f"تم بنجاح تغيير النوع الى {rstyles[int(query)]}."
                )

            return await edit_delete(
                moevent,
                f"يجب اختيار النوع بشكل صحيح\n\nهذه هي قائمة الأنواع :  [اضغط هنا]({await GetStylesGraph()}) ",
                link_preview=True,
                time=120,
            )

        return await edit_delete(
            moevent,
            f"هذه هي قائمة الأنواع :  [اضغط هنا]({await GetStylesGraph()}) ",
            link_preview=True,
            time=120,
        )
    await edit_or_reply(moevent, "جار صنع الصورة أنتظر قليلا . . .")
    getart = Somnium.Generate(query, styleid)
    await jmisbest.send_file(
        odi.chat_id,
        getart,
        force_document=True,
        reply_to=reply_to_id,
        caption=f"الـعنوان: {query}\nالنوع: {rstyles[styleid]}\n\n@jmthon",
    )
    await moevent.delete()
