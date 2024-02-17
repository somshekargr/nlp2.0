# import json
# import os

# from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data
from generate_json.table_template import get_table_data


def get_p_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_list = []
    title_data = soup_data.find(title_tag, title_tag_data)
    # for table data
    for each in get_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
        dict_list.append(each)

    # decomposing all table data, hence left with only paragraph data
    mainContent = soup_data.find(content_tag, content_tag_data)
    for table in mainContent('table'):
        table.decompose()

    # json creation for paragraph
    paragraph_value = mainContent.findAll('p')
    if len(paragraph_value) != 0:
        for para_data in paragraph_value:
            if para_data.text.strip():
                dict_list.append(generate_dict_data(
                    title_data.text.strip(), '', para_data))
            
    return dict_list

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_245.txt'), encoding="utf8"), 'html.parser')
# result_data = get_p_table_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=3))
# f = open("demofile2.json", "a")
# f.write(json.dumps(result_data, indent=3))
# f.close()
