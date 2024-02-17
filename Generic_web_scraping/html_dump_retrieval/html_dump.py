from configparser import ConfigParser
import requests
from bs4 import BeautifulSoup
config_file_path = './config.ini'
config = ConfigParser()
config.read(config_file_path)
from common.utils import get_error_details
from logger import logger_handler
logger = logger_handler.logger

base_file_name = config.get("files", "base_text_file_name")

def get_dom_text(url, path, idx):
    dom_data = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    print(url)
    response = requests.get(url,  headers=headers, proxies=None)
    if not response.ok:
        msg = f"Error while fetching the page: {response.content}"
        # raise Exception(msg)

    html = response.content
    dom = BeautifulSoup(html, features="html5lib")

    if response.status_code == 404:
        dom_data['status'] = 'Not Found'
        dom_data['title'] = None
        dom_data['file_name'] = None
        print("Not Found : " + url)
    else:
        # Gets html dom from bs
        title = dom.find('title').text
        # TODO
        title = title.replace(
            "Indian Bank | Your Own Bank :: Financial services company", "").replace("–", "").strip()

        if title is None:
            title = "IndianBank"

        # filename
        file_name = base_file_name + "_" + str(idx)
        # file_name = "".join(e for e in title if e.isalnum()) + "_" + str(idx)

        dom_data['title'] = title
        dom_data['status'] = "Found"
        dom_data['file_name'] = "{}.txt".format(file_name)

        # wrting html dump to text file
        with open("{}/{}.txt".format(path, file_name), 'w', encoding="utf-8") as html_text_file:
            html_text_file.write("%s\n" % dom)
            logger.info('Done writing html to file of ' + title)

    return dom_data


