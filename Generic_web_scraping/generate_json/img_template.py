# import json
# import os
import re

from bs4 import BeautifulSoup
from generate_json.output import generate_dict_data


def get_img_data(soup_data, title_tag, title_tag_data, content_tag, content_tag_data):
    dict_data = []
    title_data = soup_data.find(title_tag, title_tag_data).text.strip()

    main_content = soup_data.find(content_tag, content_tag_data)

    result = re.findall(
        r"(<img(.|\n)*?/><span>(.|\n)*?</span>)", str(main_content))
    final_result = [x[0] for x in result]
    print(final_result)
    for data in final_result:
        mini_soup = BeautifulSoup(data, 'html.parser')
        dict_data.append(generate_dict_data(title_data, mini_soup.find(
            'span').text.strip(), mini_soup.find('img').get('src')))

    #print(dict_data)
    return dict_data

# soup = BeautifulSoup(open(os.path.join(os.path.dirname(
#     __file__), '..', 'indianbank_data', 'indianbank_93.txt'), encoding="utf8"), 'html.parser')
# result_data = get_img_data(soup, 'innerheading', 'mainContent')
# print(json.dumps(result_data, indent=4))
