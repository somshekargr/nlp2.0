import json
import os
import re

from bs4 import BeautifulSoup

from generate_json.output import generate_dict_data


def get_list_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    main_content = soup_data.find(content_tag, content_tag_data)
    dict_data = []
    for li_data in main_content.findAll('li'):
        if li_data.text.strip():
            dict_data.append(generate_dict_data(title_data, '', li_data))
    return dict_data


# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_208.txt'), encoding="utf8"), 'html.parser')
# result_data = get_list_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=4))