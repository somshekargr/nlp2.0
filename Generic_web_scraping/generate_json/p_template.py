import json
import os
import re

from bs4 import BeautifulSoup

from generate_json.output import generate_dict_data


def get_p_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data): 
    title_data = soup_data.find(title_tag, title_tag_data)
    data = soup_data.find(content_tag, content_tag_data)
    paragraph_value = data.findAll('p')
    dict_data = []
    if len(paragraph_value) != 0:
        for i in paragraph_value:
            if i.text.strip():
                dict_data.append(generate_dict_data(title_data.text.strip(),'',i))
    return dict_data

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_231.txt'), encoding="utf8"), 'html.parser')
# result_data = get_para_data(soup,'innerheading','mainContent')
# print(json.dumps(result_data,indent=3))