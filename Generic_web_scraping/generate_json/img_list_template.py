import json
import os
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data
from generate_json.list_template import get_list_data


def get_img_list_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_data = []
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()

    main_content = soup_data.find(content_tag, content_tag_data)

    list_data =  get_list_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data)
    if list_data:
        dict_data.extend(list_data)

    img_data = main_content.findAll('img')
    if img_data:
        for img in img_data:
            dict_data.append(generate_dict_data(title_data,'',img.get('src')))

    return dict_data

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_197.txt'), encoding="utf8"), 'html.parser')
# result_data = get_img_list_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=4))