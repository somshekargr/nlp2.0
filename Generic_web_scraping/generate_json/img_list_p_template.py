import json
import os
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data

def get_img_list_p_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_data = []
    img_list = []
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    print(title_data)

    main_content = soup_data.find(content_tag, content_tag_data)
    print(main_content)

    reg_data = re.findall(r"(<p>.*?</p>(.|\n)<(ul|ol)>(.|\n)*?</(ul|ol)>)",str(main_content))
    regex_data = [x[0] for x in reg_data]
    for re_data in regex_data:
        data = BeautifulSoup(re_data,'html.parser')
        p_data = data.find('p')
        for li_data in data.findAll('li'):
            dict_data.append(generate_dict_data(title_data,p_data.text.strip(),li_data))
            for l_data in main_content.findAll('li'):
                if l_data == li_data:
                    l_data.decompose()
        for pa_data in main_content('p'):
            if pa_data == p_data:
                pa_data.decompose()
        
    for para_data in main_content.findAll('p'):
        temp_data = generate_dict_data(title_data,'',para_data)
        if temp_data['additional_data']['img']:
            img_list.append(temp_data['additional_data']['img'])
        dict_data.append(temp_data)

    img_data = main_content.findAll('img')
    img_data_list = [im.get('src') for im in img_data]

    if img_list:
        final_img_data = [
            i_data for i_data in img_data_list if i_data not in img_list]
    else:
        final_img_data = img_data_list

    if final_img_data != []:
        for image in final_img_data:
            dict_data.append(generate_dict_data(title_data, '', image))
    
    for list_data in main_content.findAll('li'):
        dict_data.append(generate_dict_data(title_data,'',list_data))

    return dict_data

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_234.txt'), encoding="utf8"), 'html.parser')
# result_data = get_img_list_p_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=4))
