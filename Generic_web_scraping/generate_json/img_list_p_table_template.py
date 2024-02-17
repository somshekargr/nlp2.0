# import json
# import os
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data
from generate_json.table_template import get_table_data


def get_img_list_p_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_data = []
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    print(title_data)

    table_data = get_table_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data)
    dict_data.extend(table_data)

    main_content = soup_data.find(content_tag, content_tag_data)
    #print(main_content)
    for table in main_content('table'):
        table.decompose()

    #print(main_content)

    pl_data = re.findall(r"(<p>.*?</p>\n<(ul|ol)>(.|\n)*?</(ul|ol)>)",str(main_content))
    final_pl_data = [data[0] for data in pl_data]
    
    if final_pl_data:
        for item in final_pl_data:
            data = BeautifulSoup(item,'html.parser')
            para_data = data.find('p')
            list_data = data.find('ul')
            for p in main_content('p'):
                if p == para_data:
                    p.decompose()
            for l in main_content('ul'):
                if l == list_data:
                    l.decompose()
            for list_item in list_data.findAll('li'):
                res_data = generate_dict_data(title_data,para_data.text.strip(),list_item.text)
                dict_data.append(res_data)
    
    print(main_content)
    p_data = main_content.findAll('p')
    for p_d in p_data:
        if p_d.text.strip():
            dict_res = generate_dict_data(title_data,'',p_d)
            dict_data.append(dict_res)

    img_data = main_content.findAll('img')
    for img in img_data:
        img_res = generate_dict_data(title_data,'',img.get('src'))
        dict_data.append(img_res)

    return dict_data

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_95.txt'), encoding="utf8"), 'html.parser')
# result_data = get_img_list_p_table_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=4))
