import asyncio
import contextlib
import os
import sys
from asyncio.exceptions import CancelledError

import heroku3
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from jmisbest import HEROKU_APP, UPSTREAM_REPO_URL, jmisbest

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)

cmdhd = Config.COMMAND_HAND_LER
ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger(__name__)

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "re-starting heroku application"
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)


# -- Constants End -- #

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**• توفر تحديث جديد للفـرت [{ac_br}]:\n\nالتغييرات:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("**• التغييرات كثيرة جدا لذلك تم وضعها في ملف**")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update_bot(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    jmthon = await event.edit("**• تم بنجاح التحديث جار اعادة التشغيل الان**")
    await event.client.reload(jmthon)


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is None:
        return await event.edit("**• يرجى وضع فار HEROKU_API_KEY للتحديث**")
    heroku = heroku3.from_key(HEROKU_API_KEY)
    heroku_applications = heroku.apps()
    if HEROKU_APP_NAME is None:
        await event.edit(
            "**• يرجى وضع فار HEROKU_APP_NAME**" " لتتمكن من تحديث السورس "
        )
        repo.__del__()
        return
    heroku_app = next(
        (app for app in heroku_applications if app.name == HEROKU_APP_NAME),
        None,
    )

    if heroku_app is None:
        await event.edit(f"{txt}\n" "**• خطأ في التعرف على تطبيق هيروكو**")
        return repo.__del__()
    jmthon = await event.edit(
        "**• جار اعادة تشغيل الدينو الان يرجى الانتظار من 2-5 دقائق**"
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [jmthon.chat_id, jmthon.id])
    except Exception as e:
        LOGS.error(e)
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_git_url = heroku_app.git_url.replace(
        "https://", f"https://api:{HEROKU_API_KEY}@"
    )

    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**تقرير الخطأ:**\n`{error}`")
        return repo.__del__()
    build_status = heroku_app.builds(order_by="created_at", sort="desc")[0]
    if build_status.status == "failed":
        return await edit_delete(
            event, "**• فشل التحديث**\n" "يبدو أنه تم الغاءه او حصل خطأ ما"
        )
    try:
        remote.push("master:main", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**تقرير الخطأ:**\n`{error}`")
        return repo.__del__()
    await event.edit("**• فشل التحديث ارسل** `.اعادة تشغيل` **للتحديث**")
    with contextlib.suppress(CancelledError):
        await event.client.disconnect()
        if HEROKU_APP is not None:
            HEROKU_APP.restart()


@jmisbest.ar_cmd(pattern="تحديث(| الان)?$")
async def upstream(event):
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(
        event, "**• جار البحث عن التحديثات يرجى الانتظار قليلا**"
    )
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if ENV and (HEROKU_API_KEY is None or HEROKU_APP_NAME is None):
        return await edit_or_reply(
            event, "**• عليك وضع فارات هيروكو المطلوبة للتحديث**"
        )
    try:
        txt = "فشل في التحديث لسورس جمثون " + "**• حدث خطأ ما :**\n"

        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\nالمجلد {error} لم يتم أيجاده")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\nفشل مبكر {error}")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"**• للأسف المجلد {error} لا يبدة انه خاص لسورس معين.\nيمكنك اصلاح هذه المشكلة بأرسال. `.تحديث التنصيب`"
            )

        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[التحديث]:**\n"
            f"يبدو أنك تستخدم فرع أخر: ({ac_br}). "
            "في هذه الحالة غير قادر على التحديث "
            "لملفات الفرع الخاص بك. "
            "يرجى استخدام الفرغ الاساسي"
        )
        return repo.__del__()
    with contextlib.suppress(BaseException):
        repo.create_remote("upstream", off_repo)
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    # Special case for deploy
    if changelog == "" and not force_update:
        await event.edit(
            "\n**• سورس جمثون محدث الى أخر اصدار**"
            f"**\n الفـرع: {UPSTREAM_REPO_BRANCH}**\n"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond(
            f"**• ارسل** `{cmdhd}تحديث التنصيب` لتحديث سورس جمثون"
        )

    if force_update:
        await event.edit("**• جار التحديث الاجباري الى اخر اصدار انتظر قليلا**")
    if conf == "الان":
        await event.edit("**• جار تحديث سورس جمثون أنتظر قليلا**")
        await update_bot(event, repo, ups_rem, ac_br)
    return


@jmisbest.ar_cmd(
    pattern="تحديث التنصيب$",
)
async def upstream(event):
    if ENV:
        if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
            return await edit_or_reply(
                event, "**• يجب عليك وضع فارات هيروكو المطلوبة للتحديث**"
            )
    elif os.path.exists("config.py"):
        return await edit_delete(
            event,
            f"**• انت تستخدم التنصيب يدويا يرجى ارسال امر** `{cmdhd}تحديث الان`",
        )
    event = await edit_or_reply(event, "**- جار جلب ملفات السورس يرجى الانتظار قليلا**")
    off_repo = "https://github.com/jmthonr/temp"
    os.chdir("/app")
    try:
        txt = "**• لقد حدث خطأ اثناء التحديث**" + "**لقد حدث خطأ ما**\n"

        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n•المجلد  {error} لم يتم ايجاده")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n• فشل مبكر الخطا: {error}")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    with contextlib.suppress(BaseException):
        repo.create_remote("upstream", off_repo)
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit("**• جار الان التحديث أنتظر قليلا**")
    await deploy(event, repo, ups_rem, ac_br, txt)
