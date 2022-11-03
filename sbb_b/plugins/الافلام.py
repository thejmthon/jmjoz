import os

from justwatch import JustWatch, justwatchapi
from pySmartDL import SmartDL

from sbb_b import sbb_b

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_or_reply

LOGS = logging.getLogger(__name__)

moviepath = os.path.join(os.getcwd(), "temp", "moviethumb.jpg")

justwatchapi.__dict__["HEADER"] = {
    "User-Agent": "JustWatch client (github.com/dawoudt/JustWatchAPI)"
}


def get_stream_data(query):
    try:
        country = Config.WATCH_COUNTRY
    except Exception:
        country = "IQ"
    # Cooking Data
    just_watch = JustWatch(country=country)
    results = just_watch.search_for_item(query=query)
    movie = results["items"][0]
    stream_data = {
        "title": movie["title"],
        "movie_thumb": (
            "https://images.justwatch.com"
            + movie["poster"].replace("{profile}", "")
            + "s592"
        ),
    }

    stream_data["release_year"] = movie["original_release_year"]
    try:
        LOGS.info(movie["cinema_release_date"])
        stream_data["release_date"] = movie["cinema_release_date"]
    except KeyError:
        try:
            stream_data["release_date"] = movie["localized_release_date"]
        except KeyError:
            stream_data["release_date"] = None

    stream_data["type"] = movie["object_type"]

    available_streams = {}
    for provider in movie["offers"]:
        provider_ = get_provider(provider["urls"]["standard_web"])
        available_streams[provider_] = provider["urls"]["standard_web"]

    stream_data["providers"] = available_streams

    scoring = {}
    for scorer in movie["scoring"]:
        if scorer["provider_type"] == "tmdb:score":
            scoring["tmdb"] = scorer["value"]

        if scorer["provider_type"] == "imdb:score":
            scoring["imdb"] = scorer["value"]
    stream_data["score"] = scoring
    return stream_data


# Helper Functions
def pretty(name):
    if name == "play":
        name = "Google Play Movies"
    return name[0].upper() + name[1:]


def get_provider(url):
    url = url.replace("https://www.", "")
    url = url.replace("https://", "")
    url = url.replace("http://www.", "")
    url = url.replace("http://", "")
    url = url.split(".")[0]
    return url


@sbb_b.ar_cmd(pattern="فلم ([\s\S]*)")
async def _(event):
    query = event.pattern_match.group(1)
    et = await edit_or_reply(event, "**- جار البحث في المواقع انتظر قليلا**")
    try:
        streams = get_stream_data(query)
    except Exception as e:
        return await et.edit(f"**خطأ :** `{e}`")
    title = streams["title"]
    thumb_link = streams["movie_thumb"]
    release_year = streams["release_year"]
    release_date = streams["release_date"]
    scores = streams["score"]
    try:
        imdb_score = scores["imdb"]
    except KeyError:
        imdb_score = None
    try:
        tmdb_score = scores["tmdb"]
    except KeyError:
        tmdb_score = None

    stream_providers = streams["providers"]
    if release_date is None:
        release_date = release_year

    output_ = f"**الفلم:**\n`{title}`\n**تاريخ الصدور:**\n`{release_date}`"
    if imdb_score:
        output_ = f"{output_}\n**IMDB: **{imdb_score}"
    if tmdb_score:
        output_ = f"{output_}\n**TMDB: **{tmdb_score}"

    output_ = output_ + "\n\n**متاح على:**\n"
    for provider, link in stream_providers.items():
        if "sonyliv" in link:
            link = link.replace(" ", "%20")
        output_ += f"[{pretty(provider)}]({link})\n"
    downloader = SmartDL(thumb_link, moviepath, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    await event.client.send_file(
        event.chat_id,
        caption=output_,
        file=moviepath,
        force_document=False,
        allow_cache=False,
        silent=True,
    )
    await et.delete()
