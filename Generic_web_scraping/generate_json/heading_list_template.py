# import json
# import os
import re

from bs4 import BeautifulSoup

from generate_json.output import generate_dict_data

header_list = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']


def get_heading_list_data(html_data, title_tag, title_tag_data, content_tag, content_tag_data):
    title_data = html_data.find(title_tag, title_tag_data).text.strip()
    print(title_data)
    data = html_data.find(content_tag, content_tag_data)
    total_list = data.findAll('ul')
    result = re.findall(
        r"(<h[1-6]>.*?</h[1-6]>(.|\n)<ul>(.|\n)*?</ul>)", str(data))
    result_data = [data for x in result for data in x if data != '\n']
    #print(result_data)
    json_list = []
    ul_items = []
    if result_data != []:
        for list_item in result_data:
            converted_data = BeautifulSoup(list_item, 'html.parser')
            tag_list = sorted(list(
                set(tag.name for tag in converted_data.find_all() if tag.name in header_list)))
            if len(tag_list) >= 1:
                heading_data = converted_data.find(tag_list[0])
                list_data = converted_data.find_all('ul')
                ul_items.extend(list_data)
                for item in list_data:
                    list_value = item.findAll('li')
                    for i in list_value:
                        json_list.append(generate_dict_data(
                            title_data, heading_data.text.strip(), i))
    if len(ul_items) != len(total_list):
        final_list = [li for li in total_list if li not in ul_items]
        print(final_list)
        if len(final_list) != 0:
            for li_item in final_list:
                li_value = li_item.findAll('li')
                for j in li_value:
                    json_list.append(generate_dict_data(
                        title_data, '', j))

    return json_list


# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_162.txt'), encoding="utf8"), 'html.parser')
# # print(soup.text)
# final_result = get_heading_list_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(final_result, indent=3))
# print(soup.find('div', 'mainContent'))
