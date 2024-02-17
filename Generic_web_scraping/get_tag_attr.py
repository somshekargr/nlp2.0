
import requests
from bs4 import BeautifulSoup


def get_tag_with_attr(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'X-Requested-With': 'XMLHttpRequest',
    }

    response = requests.get(url,  headers=headers, proxies=None)
    if not response.ok:
        msg = f"Error while fetching the page: {response.content}"
        # raise Exception(msg)

    html = response.content
    soup = BeautifulSoup(html, "html.parser")

    body = soup.find('body')

    tags = []
    for tag in body.find_all():
        attrs = tag.attrs
        tagName = tag.name
        tags.append({tagName: attrs})

    return tags
    # print(tags)
