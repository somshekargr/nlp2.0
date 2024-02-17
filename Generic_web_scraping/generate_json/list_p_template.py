# import json
# import os
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data


def get_list_p_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_data = []
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    print(title_data)

    main_content = soup_data.find(content_tag, content_tag_data)
    #print(main_content)

    regex_data = re.findall(r"(<p.*?>.*?</p>(.|\n)<(ul|ol).*?>(.|\n)*?</(ul|ol)>)",str(main_content))
    reg_data = [x[0] for x in regex_data]

    #print(reg_data)
    for res_data in reg_data:
        temp_soup = BeautifulSoup(res_data, 'html.parser')
        heading_data = temp_soup.find('p')
        list_data = temp_soup.find_all('li')
        if list_data:
            for li_item in main_content.findAll('li'):
                if li_item in list_data:
                    dict_data.append(generate_dict_data(
                        title_data, heading_data.text.strip(), li_item))
                    li_item.decompose()
        if heading_data:
            for head_data in main_content.findAll('p'):
                if head_data == heading_data:
                    head_data.decompose()
    
    for pa_data in main_content.findAll('p'):
        if pa_data.text.strip():
            dict_data.append(generate_dict_data(title_data, '', pa_data))
        pa_data.decompose()

    for li_data in main_content.findAll('li'):
        if li_data.text.strip():
            dict_data.append(generate_dict_data(title_data, '', li_data))
        li_data.decompose()

    #print(main_content)

    return dict_data



# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#      __file__), '..', 'indianbank_data', 'indianbank_249.txt'), encoding="utf8"), 'html.parser')

# result_data = get_list_p_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=3)) 
