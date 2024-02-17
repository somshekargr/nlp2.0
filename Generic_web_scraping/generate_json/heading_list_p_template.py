import json
import os
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data




def get_heading_list_p_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_data = []
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    print(title_data)

    mainContent = soup_data.find(content_tag, content_tag_data)
    #print(mainContent)
    result = re.findall(
        r"(<h[1-6].*?>.*?</h[1-6]>(.|\n)(<p>(.|\n)*?</p>|<(ul|ol)>(.|\n)*?</(ul|ol)>))", str(mainContent))
    # result = mainContent.findAll(re.compile('(ul|ol)'))
    result_data = [x[0] for x in result]
    print(len(result_data))
    for res_data in result_data:
        temp_soup = BeautifulSoup(res_data, 'html.parser')
        heading_data = temp_soup.find(re.compile("^h[1-6]$"))
        para_data = temp_soup.find('p')
        list_data = temp_soup.find_all('li')
        if para_data:
            for p_d in mainContent.findAll('p'):
                if p_d == para_data:
                    dict_data.append(generate_dict_data(
                        title_data, heading_data.text.strip(), para_data))
                    p_d.decompose()
        if list_data:
            for li_item in mainContent.findAll('li'):
                if li_item in list_data:
                    dict_data.append(generate_dict_data(
                        title_data, heading_data.text.strip(), li_item))
                    li_item.decompose()
        for heading_data in mainContent.findAll(re.compile("^h[1-6]$")):
            heading_data.decompose()

    for head_data in mainContent.findAll(re.compile("^h[1-6]$")):
        dict_data.append(generate_dict_data(title_data, '', head_data))
        head_data.decompose()

    for pa_data in mainContent.findAll('p'):
        dict_data.append(generate_dict_data(title_data, '', pa_data))
        pa_data.decompose()

    for li_data in mainContent.findAll('li'):
        dict_data.append(generate_dict_data(title_data, '', li_data))
        li_data.decompose()

    #print(mainContent)

    return dict_data

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_188.txt'), encoding="utf8"), 'html.parser')
# result_data = get_heading_list_p_table_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=4))
