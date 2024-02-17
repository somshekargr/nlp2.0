from bs4 import BeautifulSoup
import re
import os
from collections import defaultdict
import shutil
from configparser import ConfigParser
import ast
from datetime import datetime

config_file_path = './config.ini'
config = ConfigParser()
config.read(config_file_path)
# path = 'E:/D DRIVE/BotWorkSpace/WebScraping/document'
# files_data = os.listdir(path)
# dir_path = os.path.relpath(path)
# print(dir_path)
# print(files_data)
tag_list = ast.literal_eval(config.get("classifiction", "tag_list"))
header_list = ast.literal_eval(config.get("classifiction", "header_list"))
table_list = ast.literal_eval(config.get("classifiction", "table_list"))
hlist_list = ast.literal_eval(config.get("classifiction", "hlist_list"))
CONTENT = config.get("classifiction", "content_class")


def html_classification(path, csv_file_path):
    try:
        files_data = os.listdir(path)
        dir_path = os.path.relpath(path)
        files_dict = {}
        for file_name in files_data:
            soup = BeautifulSoup(
                open(f'./{dir_path}/{file_name}', encoding="utf8"), 'html.parser')
            # print(soup.find_all('randomContent'))
            # print(soup.body.prettify())
            regex = re.compile(CONTENT)
            data = soup.find('div', {'class': regex})
            if data != None:
                temp_list = sorted(
                    set([tag.name for tag in data.find_all() if tag.name not in tag_list]))
                temp_list_1 = sorted(
                    set(list(map(lambda x: 'table' if x in table_list else x, temp_list))))
                temp_list_2 = sorted(
                    set(list(map(lambda x: 'list' if x in hlist_list else x, temp_list_1))))
                files_dict[file_name] = ' '.join(
                    sorted(set(list(map(lambda x: 'heading' if x in header_list else x, temp_list_2)))))
            else:
                files_dict[file_name] = ''

        # print(files_dict)
        classification_data = defaultdict(list)
        for key, value in sorted(files_dict.items()):
            classification_data[value].append(key)
        # print(len(classification_data))
        for key, value in classification_data.items():
            print(f'{key}  {len(value)}')
        classify_to_folders = files_to_folders(classification_data, dir_path, csv_file_path)
        print(classify_to_folders)
        return classify_to_folders
    
    except Exception as e:
        print(e)
        return False
    #print(json.dumps(classification_data, indent=4))


def files_to_folders(dict_data, dir_path, csv_file_path):
    now = datetime.now()
    try:
        if os.path.exists("files") is False:
            os.mkdir("files")
        classification_main = os.path.join("files", "classified_files")
        if os.path.exists(classification_main) is False:
            os.mkdir(classification_main)
        date_path = os.path.join(
            classification_main, now.strftime("%m_%d_%Y_%H_%M_%S"))
        if os.path.exists(date_path) is False:
            os.mkdir(date_path)
        classified_path = os.path.join(date_path, "classifications")
        if os.path.exists(classified_path) is False:
            os.mkdir(classified_path)
        # os.mkdir("classified_files")
        count = 0
        for key, value in dict_data.items():
            if key != '':
                os.mkdir(f'{classified_path}/temp_{count}_{key}')
                shutil.copy(f'./dump_classifiction/init_config.ini',
                            f'{classified_path}/temp_{count}_{key}')
                f = open(
                    f'{classified_path}/temp_{count}_{key}/init_config.ini', "a")
                f.write(key)
                f.close()
                for val in value:
                    shutil.copy(f'./{dir_path}/{val}',
                                f'{classified_path}/temp_{count}_{key}/{val}')

                count = count + 1
            else:
                os.mkdir(f'{classified_path}/temp_none')
                for val in value:
                    shutil.copy(f'./{dir_path}/{val}',
                                f'{classified_path}/temp_none/{val}')

        shutil.make_archive(date_path+"/classifications", 'zip', classified_path)
        return {"folder_path": classified_path,
                "zip_path": '{}/classifications.zip'.format(date_path),
                "csv_file_path" : csv_file_path}
        
    except Exception as e:
        print(e)
        return False


# html_classification(path)
