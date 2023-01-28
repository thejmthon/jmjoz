import math
import time

import heroku3
import requests

from ...Config import Config
from .utils import get_readable_time

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

# UniBorg Telegram UseRBot
# Copyright (C) 2020 @UniBorg
# This code is licensed under
# the "you can't use this for anything - public or private,
# unless you know the two prime factors to the number below" license
# 543935563961418342898620676239017231876605452284544942043082635399903451854594062955
# വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ
# ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!
# uniborg


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "لم يتم وضع قاعدة بيانات"
    if not Config.DB_URI:
        return is_database_working, output
    from ...sql_helper import SESSION

    try:
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {e}"
        is_database_working = False
    else:
        output = "تعمل بنجاح"
        is_database_working = True
    return is_database_working, output


async def jmthonalive(StartTime):
    _, check_sgnirts = check_data_base_heal_th()
    sudo = "موجود" if Config.SUDO_USERS else "غير موجود"
    uptime = await get_readable_time((time.time() - StartTime))
    try:
        useragent = (
            "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/80.0.3987.149 Mobile Safari/537.36"
        )
        user_id = Heroku.account().id
        headers = {
            "User-Agent": useragent,
            "Authorization": f"Bearer {Config.HEROKU_API_KEY}",
            "Accept": "application/vnd.heroku+json; version=3.account-quotas",
        }
        path = f"/accounts/{user_id}/actions/get-quota"
        r = requests.get(heroku_api + path, headers=headers)
        result = r.json()
        quota = result["account_quota"]
        quota_used = result["quota_used"]

        # Used
        remaining_quota = quota - quota_used
        math.floor(remaining_quota / quota * 100)
        minutes_remaining = remaining_quota / 60
        hours = math.floor(minutes_remaining / 60)
        minutes = math.floor(minutes_remaining % 60)
        # Current
        App = result["apps"]
        try:
            App[0]["quota_used"]
        except IndexError:
            AppQuotaUsed = 0
        else:
            AppQuotaUsed = App[0]["quota_used"] / 60
            math.floor(App[0]["quota_used"] * 100 / quota)
        AppHours = math.floor(AppQuotaUsed / 60)
        AppMinutes = math.floor(AppQuotaUsed % 60)
        dyno = f"{AppHours}h {AppMinutes}m/{hours}h {minutes}m"
    except Exception as e:
        dyno = e
    return f"🖤༄ سورس جمثون ༄🖤\
                 \n\nღ ثاعدة البيانات : {check_sgnirts}\
                  \nღ المطور الثانوي : {sudo}\
                  \nღ الوقت : {uptime}\
                  \nღ الدينو : {dyno}\
                  "
