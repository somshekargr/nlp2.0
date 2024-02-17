from bs4 import BeautifulSoup
import re
import json
import os
from generate_json.output import generate_dict_data
from generate_json.table_template import get_table_data
from generate_json.list_template import get_list_data


def get_list_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_list = []
    title_data = soup_data.find(title_tag, title_tag_data)
    # for table data
    for each in get_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
        dict_list.append(each)

    # decomposing all table data, hence left with only list data
    mainContent = soup_data.find(content_tag, content_tag_data)
    for table in mainContent('table'):
        table.decompose()

    # json creation for list data
    list_values = mainContent.findAll('li')
    if len(list_values) != 0:
        for i in list_values:
            dict_list.append(generate_dict_data(
                title_data.text.strip(), '', i))
            
    return dict_list

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_184.txt'), encoding="utf8"), 'html.parser')

# result_data = get_list_table_data(soup, 'innerheading', 'mainContent')
    
# print(json.dumps(result_data,indent=3))
