import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import re
from logger import logger_handler
logger = logger_handler.logger


def find_hrfs_url(url, regUrl):
    urls = []
    urlRx = re.compile(regUrl)
    headers = {
        'Accept': 'text/html',  # Set the appropriate content type you expect
    }

    page = requests.get(url, headers=headers)
    if page.ok:
        soup = BeautifulSoup(page.content, 'html.parser',
                             from_encoding="iso-8859-1")

        links = soup.find_all('a', href=True)
        for link in links:
            currentURL = link['href']

            if has_extension_in_url(currentURL) is False:
                if urlRx.search(currentURL) is not None:
                    urls.append(currentURL)

        urls = list(set(urls))
        return urls

    elif page.status_code == 404:
        logger.info(url, page.reason)
        return None

    elif page.status_code == 406:
        logger.info(url, page.reason)
        return None

    else:
        logger.error(
            "Sorry, could not get from {} : {}".format(url, page.reason))
        raise Exception(
            "Sorry, could not get from {} : {}".format(url, page.reason))


def get_urls(url):
    site_map = {}
    url_links = []
    doc_links = []
    regUrl = url

    # level_1_parent = url
    # level_1_urls = []
    urls = find_hrfs_url(url, regUrl)
    if urls is not None:
        for each in urls:
            url_links.append({'parent': url, 'child': each.replace("#!", "")})
            # level_1_urls.append(each)

            links = find_hrfs_url(each, regUrl)
            if (links):
                for link in links:
                    url_links.append(
                        {'parent': each, 'child': link.replace("#!", "")})
            elif (links is None):
                url_links.append(
                    {'parent': url, 'child': each.replace("#!", "")})

        site_map['url_links'] = list(
            {val['child']: val for val in url_links}.values())
        logger.info("Number of url links found {}".format(
            len(site_map['url_links'])))

        for each_link in site_map['url_links']:
            docs_link = get_doc_links(each_link['child'])
            if (docs_link):
                for each in docs_link:
                    doc_links.append(each)

        site_map['doc_links'] = list(set(doc_links))
        logger.info("Number of url links found {}".format(
            len(site_map['doc_links'])))

        return site_map
    return None


def get_doc_links(url):
    urls = []
    page = requests.get(url)
    if page.ok:
        soup = BeautifulSoup(page.content, 'html.parser',
                             from_encoding="iso-8859-1")

        links = soup.find_all('a', href=True)
        for link in links:
            currentURL = link['href']

            if ('.pdf' in currentURL or '.txt' in currentURL or '.xls' in currentURL or '.xlsx'):
                urls.append(currentURL)

        urls = list(set(urls))
        return urls

    elif page.status_code == 404:
        logger.info(url, page.reason)
        return None

    else:
        logger.error(
            "Sorry, could not get from {} : {}".format(url, page.reason))
        raise Exception(
            "Sorry, could not get from {} : {}".format(url, page.reason))

def has_extension_in_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    file_extension = os.path.splitext(path)[1]
    return bool(file_extension)
