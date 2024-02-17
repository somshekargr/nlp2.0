import json
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data
from generate_json.table_template import get_table_data

header_list = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

def get_heading_table_data(html_data, title_tag, title_tag_data, content_tag, content_tag_data):
    title_data = html_data.find(title_tag, title_tag_data).text.strip()
    print(title_data)
    
    data = html_data.find(content_tag, content_tag_data)

    pattern_data = re.findall(r"(<h[1-6]>.*?</h[1-6]>(.|\n)<table .*?>(.|\n)*?</table>)",str(data))
    final_pattern_data = [data for x in pattern_data for data in x if data != '\n']
    json_list = []
    table_items = []
    if final_pattern_data != []:
        for list_item in final_pattern_data:
            converted_data = BeautifulSoup(list_item, 'html.parser')
            tag_list = sorted(list(
                set(tag.name for tag in converted_data.find_all() if tag.name in header_list)))
            if len(tag_list) >= 1:
                heading_data = converted_data.find(tag_list[0])
                list_table_data = converted_data.find_all('table')
                table_items.extend(list_table_data)
                for item in list_table_data:
                    json_list.append(generate_dict_data(
                        title_data.text.strip(), heading_data.text.strip(), item))
    else:
        json_list.extend(get_table_data(html_data, title_tag, title_tag_data, content_tag, content_tag_data))
    return json_list

# soup = BeautifulSoup(open(
#     './indianbank_data/indianbank_232.txt'), 'html.parser')
# result = get_heading_table_data(soup,'innerheading','mainContent')
# print(json.dumps(result,indent=4))