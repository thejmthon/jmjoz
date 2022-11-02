import os
import re

import requests

try:
    from pyquery import PyQuery as pq
except ModuleNotFoundError:
    os.system("pip3 install pyquery")
    from pyquery import PyQuery as pq


def get_download_url(link):
    post_request = requests.post(
        "https://www.expertsphp.com/download.php", data={"url": link}
    )

    request_content = post_request.content
    str_request_content = str(request_content, "utf-8")
    download_url = pq(str_request_content)("table.table-condensed")("tbody")("td")(
        "a"
    ).attr("href")
    return download_url


def get_msg_button(texts: str):
    btn = []
    for z in re.findall("\\[(.*?)\\|(.*?)\\]", texts):
        text, url = z
        urls = url.split("|")
        url = urls[0]
        # if not is_url_ok(url):
        #    continue
        if len(urls) > 1:
            btn[-1].append([text, url])
        else:
            btn.append([[text, url]])

    txt = texts
    for z in re.findall("\\[.+?\\|.+?\\]", texts):
        txt = txt.replace(z, "")

    return txt.strip(), btn
