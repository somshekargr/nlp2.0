import json
import os
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data


def get_heading_img_p_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_data = []
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()
    #print(title_data)

    main_content = soup_data.find(content_tag, content_tag_data)
    #print(main_content)
    result_1 = re.findall(r'(<img.*?>(.|\n).*?<strong>.*?</strong>(.|\n)*?<br/>(.|\n).*?<br/>)',str(main_content))
    if result_1:
        result_1_data = [x[0] for x in result_1]
        for img_data in result_1_data:
            img_soup = BeautifulSoup(img_data, 'html.parser')
            heading_data = img_soup.text.strip()
            img_src_value = img_soup.find('img').get('src')
            dict_data.append(generate_dict_data(title_data,heading_data,img_src_value))


    #<img.*?>(.|\n).*?<strong>.*?</strong>(.|\n)*?<br/>(.|\n).*?<br/>
    result_2 = re.findall(r'(<p.*?>(.|\n)*?</p>(.|\n)*?<h[1-6].*?>.*</h[1-6]>{1,}(.|\n)(<p((.|\n)*?)>.*?</p>(.|\n)){1,})',str(main_content))
    if result_2:
        result_2_data = [y_data[0] for y_data in result_2]
        for regex_data_1 in result_2_data:
            regex_data_value = BeautifulSoup(regex_data_1, 'html.parser')
            heading_d = regex_data_value.find_all(re.compile("^h[1-6]$"))
            _heading_data = heading_d[0].text.strip()
            final_heading_list = heading_d[1:]
            for heading in final_heading_list:
                dict_data.append(generate_dict_data(title_data,_heading_data,heading.text.strip()))
            para_data = regex_data_value.find_all('p')
            for _para in para_data:
                dict_data.append(generate_dict_data(title_data,_heading_data,_para))
            # dict_data.append(generate_dict_data(title_data,heading_data,img_src_value))

    return dict_data


# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_31.txt'), encoding="utf8"), 'html.parser')
# result_data = get_heading_img_p_data(
#     soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=4))
