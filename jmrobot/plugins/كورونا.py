from covid import Covid

from . import covidindia, edit_delete, edit_or_reply, jmrobot


@jmrobot.ar_cmd(pattern="كورونا(?:\s|$)([\s\S]*)")
async def corona(event):
    input_str = event.pattern_match.group(1)
    country = (input_str).title() if input_str else "iraq"
    rozevent = await edit_or_reply(event, "⌯︙يتـم سـحب الـمعلومات")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n⌯︙الاصابات المؤكده : <code>{hmm1}</code>"
        data += f"\n⌯︙الاصابات المشبوهه : <code>{country_data['active']}</code>"
        data += f"\n⌯︙الوفيات : <code>{hmm2}</code>"
        data += f"\n⌯︙الحرجه : <code>{country_data['critical']}</code>"
        data += f"\n⌯︙حالات الشفاء : <code>{country_data['recovered']}</code>"
        data += f"\n⌯︙اجمالي الاختبارات : <code>{country_data['total_tests']}</code>"
        data += f"\n⌯︙الاصابات الجديده : <code>{country_data['new_cases']}</code>"
        data += f"\n⌯︙الوفيات الجديده : <code>{country_data['new_deaths']}</code>"
        await rozevent.edit(
            "<b>⌯︙معـلومات كـورونا لـ {}:\n{}</b>".format(country, data),
            parse_mode="html",
        )
    else:
        data = await covidindia(country)
        if data:
            roz1 = int(data["new_positive"]) - int(data["positive"])
            roz2 = int(data["new_death"]) - int(data["death"])
            roz3 = int(data["new_cured"]) - int(data["cured"])
            result = f"<b>Corona virus info of {data['state_name']}\
                \n⌯︙الاصابات المؤكده : <code>{data['new_positive']}</code>\
                \n⌯︙الاصابات المشبوهه : <code>{data['new_active']}</code>\
                \n⌯︙الوفيات : <code>{data['new_death']}</code>\
                \n⌯︙حالات الشفاء : <code>{data['new_cured']}</code>\
                \n⌯︙اجمالي الاختبارات  : <code>{roz1}</code>\
                \n⌯︙الحالات الجديده : <code>{roz2}</code>\
                \n⌯︙الوفيات الجديده : <code>{roz3}</code> </b>"
            await rozevent.edit(result, parse_mode="html")
        else:
            await edit_delete(
                rozevent,
                "**⌯︙معلومات فايروس كورونا في - {} غير متوفره**".format(country),
                5,
            )
