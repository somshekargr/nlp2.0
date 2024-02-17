import json
import os
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data

def get_heading_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_data = []
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    print(title_data)

    main_content = soup_data.find(content_tag, content_tag_data)

    #print(mainContent)

    for heading in main_content.findAll(re.compile("^h[1-6]$")):
        dict_data.append(generate_dict_data(title_data,'',heading))
        heading.decompose()

    return dict_data

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_188.txt'), encoding="utf8"), 'html.parser')
# result_data = get_heading_list_p_table_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=4))
