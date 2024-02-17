import json
import os
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data

header_list = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']


def get_heading_p_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    print(title_data)
    
    data = soup_data.find(content_tag, content_tag_data)
    total_para = data.findAll('p')
    result = re.findall(
        r"(<h[1-6]>.*?</h[1-6]>(.|\n)<p>(.|\n)*?</p>)", str(data))
    temp_result = [data for x in result for data in x if data != '\n']
    result_data = [x for x in temp_result if x != '>']
    #print(result_data)
    json_list = []
    para_items = []
    if result_data != []:
        for list_item in result_data:
            converted_data = BeautifulSoup(list_item, 'html.parser')
            tag_list = sorted(list(
                set(tag.name for tag in converted_data.find_all() if tag.name in header_list)))
            if len(tag_list) >= 1:
                heading_data = converted_data.find(tag_list[0])
                para_data = converted_data.find_all('p')
                para_items.extend(para_data)
                for item in para_data:
                    json_list.append(generate_dict_data(
                        title_data, heading_data.text.strip(), item))
    if len(para_items) != len(total_para):
        final_para_list = [p for p in total_para if p not in para_items]
        print(final_para_list)
        if len(final_para_list) != 0:
            for para_item in final_para_list:
                json_list.append(generate_dict_data(
                    title_data, '', para_item.text.strip()))
    return json_list


# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_85.txt'), encoding="utf8"), 'html.parser')
# resultData = get_heading_p_data(soup,'innerheading','mainContent')
# print(json.dumps(resultData,indent=4))