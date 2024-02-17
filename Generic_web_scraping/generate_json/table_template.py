import json
import os
import re

from bs4 import BeautifulSoup

from generate_json.output import generate_dict_data

# TODO for inner table data logic needs to changed


def get_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    print(title_data)

    main_content = soup_data.find(content_tag, content_tag_data)
    dict_list = []
    table_data = main_content.findAll('table')
    #print(len(table_data))
    # TODO need to check with max_table_size logic for inner table
    for table in table_data:
        max_table_size = max([len(row.findAll('td'))
                             for row in table.findAll('tr')])
        #print(max_table_size)

        if max_table_size == 2:
            for each in get_size_two_table_data(table, title_data):
                dict_list.append(each)
        else:
            temp_list = []
            for row in table.findAll('tr'):
                temp_dict = {}

                col_data = row.findAll('td')
                for col in range(0, len(col_data)):
                    temp_dict[f"col{col}"] = col_data[col].text
                temp_list.append(temp_dict)

            dict_list.append(generate_dict_data(title_data, '', '', temp_list))

    return dict_list


def get_size_two_table_data(table_data, title, predicate_index=0, object_index=1):
    dict_list = []
    for item in table_data.select('table tr'):
        if len(item) > 0:
            # handiling special case
            if len(item.find_all('td')) <= 1:
                if item.find_all('td'):
                    if len(dict_list) == 0:
                        object_index = 0
                        dict_list.append(generate_dict_data(
                            title, '', item.select('td')[object_index].text.strip()))
                    else:
                        object_index = 0
                        dict_list.append(generate_dict_data(
                            title, dict_list[0]['pedicate'], item.select('td')[object_index].text.strip()))
            else:
                object_index = 1
                dict_list.append(generate_dict_data(
                    title, item.select('td')[predicate_index].text.strip(), item.select('td')[object_index].text.strip()))

    return dict_list


# #For Testing Purpose
# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_237.txt'), encoding="utf8"), 'html.parser')
# result_data = get_table_data(soup,'innerheading','mainContent')
# print(json.dumps(result_data,indent=3))
