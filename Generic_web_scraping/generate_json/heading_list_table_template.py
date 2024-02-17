import json
import os
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data
from generate_json.table_template import get_table_data

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_171.txt'), encoding="utf8"), 'html.parser')


def get_heading_list_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_data = []
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    print(title_data)

    table_data = get_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data)
    dict_data.extend(table_data)

    main_content = soup_data.find(content_tag, content_tag_data)

    for table in main_content.findAll('table'):
        table.decompose()

    result = re.findall(
        r"(<h[1-6].*?>.*?</h[1-6]>(.|\n)<(ul|ol)>(.|\n)*?</(ul|ol)>)", str(main_content))
    # result = mainContent.findAll(re.compile('(ul|ol)'))
    result_data = [x[0] for x in result]
    print(len(result_data))
    for res_data in result_data:
        temp_soup = BeautifulSoup(res_data, 'html.parser')
        heading_data = temp_soup.find(re.compile("^h[1-6]$"))
        list_data = temp_soup.find_all('li')
        if list_data:
            for li_item in main_content.findAll('li'):
                if li_item in list_data:
                    dict_data.append(generate_dict_data(
                        title_data, heading_data.text.strip(), li_item))
                    li_item.decompose()
        for heading_data in main_content.findAll(re.compile("^h[1-6]$")):
            heading_data.decompose()

    for heading in main_content.findAll(re.compile("^h[1-6]$")):
        dict_data.append(generate_dict_data(title_data,'',heading))
        heading.decompose()

    for list_data in main_content.findAll('li'):
        if list_data.text.strip():
            dict_data.append(generate_dict_data(title_data,'',list_data))
        list_data.decompose()

    return dict_data


# result_data = get_heading_list_table_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=4))
