import json

import requests

from . import edit_delete, edit_or_reply, jmrobot


@jmrobot.ar_cmd(pattern="صلاة(?:\s|$)([\s\S]*)")
async def get_adzan(adzan):
    adzan.pattern_match.group(1)
    LOKASI = adzan.pattern_match.group(1)
    url = f"https://api.pray.zone/v2/times/today.json?city={LOKASI}"
    request = requests.get(url)
    if request.status_code != 200:
        await edit_delete(
            adzan,
            f"** لم يتم العثور على معلومات لهذه المدينه {LOKASI}**\n يرجى كتابة اسم محافظتك وباللغه الانكليزي ",
            15,
        )  # ترجمه فريق جمثون على التيلكرام
        return
    result = json.loads(request.text)
    jmrobotresult = f"<b>اوقات صلاه المسلمين 👳‍♂️ </b>\
            \n\n<b>المدينة     : </b><i>{result['results']['location']['city']}</i>\
            \n<b>الدولة  : </b><i>{result['results']['location']['country']}</i>\
            \n<b>التاريخ     : </b><i>{result['results']['datetime'][0]['date']['gregorian']}</i>\
            \n<b>الهجري    : </b><i>{result['results']['datetime'][0]['date']['hijri']}</i>\
            \n\n<b>الامساك    : </b><i>{result['results']['datetime'][0]['times']['Imsak']}</i>\
            \n<b>شروق الشمس  : </b><i>{result['results']['datetime'][0]['times']['Sunrise']}</i>\
            \n<b>الفجر     : </b><i>{result['results']['datetime'][0]['times']['Fajr']}</i>\
            \n<b>الظهر    : </b><i>{result['results']['datetime'][0]['times']['Dhuhr']}</i>\
            \n<b>العصر      : </b><i>{result['results']['datetime'][0]['times']['Asr']}</i>\
            \n<b>غروب الشمس   : </b><i>{result['results']['datetime'][0]['times']['Sunset']}</i>\
            \n<b>المغرب  : </b><i>{result['results']['datetime'][0]['times']['Maghrib']}</i>\
            \n<b>العشاء     : </b><i>{result['results']['datetime'][0]['times']['Isha']}</i>\
            \n<b>منتصف الليل : </b><i>{result['results']['datetime'][0]['times']['Midnight']}</i>\
    "
    await edit_or_reply(adzan, jmrobotresult, "html")
