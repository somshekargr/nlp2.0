import json
import os

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data
from generate_json.p_template import get_p_data
from generate_json.table_template import get_table_data


def get_img_p_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_data = []
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    #print(title_data)

    table_data = get_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data)
    dict_data.extend(table_data)

    main_content = soup_data.find(content_tag, content_tag_data)
    #print(main_content)
    for table in main_content('table'):
        table.decompose()


    img_data = main_content.findAll('img')
    img_data_list = [im.get('src') for im in img_data]
    img_para_data = get_p_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data)

    if img_para_data:
        img_data_para = [data['additional_data']['img']
                         for data in img_para_data if data['additional_data']['img'] != '']

    if img_data_para:
        final_img_data = [
            i_data for i_data in img_data_list if i_data not in img_data_para]
    else:
        final_img_data = img_data_list

    if final_img_data != []:
        for image in final_img_data:
            img_para_data.append(generate_dict_data(title_data, '', image))

    dict_data.extend(img_para_data)

    return dict_data

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_61.txt'), encoding="utf8"), 'html.parser')
# result_data = get_img_p_table_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=4))
