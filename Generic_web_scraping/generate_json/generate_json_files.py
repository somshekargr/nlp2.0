import csv
import json
import os
import sys
from configparser import ConfigParser

from generate_json.final_templates import *
from bs4 import BeautifulSoup
from utils.csv_search import search_csv
from utils.elastic_data_dump import ElasticSearchClient

sys.path.insert(1, '/path/to/mod_directory')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def read_ini_file(filename):
    # Create a ConfigParser object
    config = ConfigParser()

    # Read the INI file
    config.read(filename)

    # Convert the ConfigParser object to a dictionary
    data = {}
    for section in config.sections():
        data[section] = {}
        for key, value in config.items(section):
            data[section][key] = value

    return data


config_file = read_ini_file('.env')
#print(config_file)

es_host = config_file['elastic_search_credentials']['host']
es_port = int(config_file['elastic_search_credentials']['port'])
es_index = config_file['elastic_search_credentials']['index']
es_user = config_file['elastic_search_credentials']['user']
es_password = config_file['elastic_search_credentials']['password']
es = ElasticSearchClient(es_host, es_port, es_index, '_doc',es_user,es_password)


def generate_json_files(classified_file_path, csv_file_path ):
    """
    Recursively gets all files in a directory and its subdirectories.
    """
    with open(f'{config_file["application"]["template_dict_path"]}') as f:
        json_data = json.load(f)

    # path = os.path.abspath(config_file['application']['path'])
    # TODO change to dynamic path
    path = os.path.abspath(classified_file_path)
    sub_dir_list = os.listdir(path)
    pos_count = 0
    neg_count = 0

    # deleting previous index for new insertion of docuemnts
    if es.check_connection():
        es.delete_index()
    else:
        print("ElasticSearch index deletion failed.")
        return

    for sub_dir in sub_dir_list:
        if sub_dir != 'temp_none':
            for root, dir, filenames in os.walk(os.path.join(path, sub_dir)):
                config_index = filenames.index('init_config.ini')
                config_file_data = read_ini_file(
                    os.path.join(root, filenames[config_index]))
                template_data = config_file_data['application']['key'].replace(
                    ' ', '_').strip()
                template_data = template_data + '_template'
                template_function = search_key(json_data, template_data)
                filenames.pop(config_index)
                for FILES in filenames:
                    if config_file['csvdata']['search_key']:
                        file_data = search_csv(csv_file_path, config_file['csvdata']['search_key'], FILES)[0]
                    else:
                        file_data = ''
                    soup_data = BeautifulSoup(
                        open(os.path.join(root, FILES), encoding="utf8"), 'html.parser')
                    final_data = eval(template_function)(soup_data, str(config_file['application']['title_content_tag']),str(config_file['application']['title_content']),str(config_file['application']['main_content_tag']), str(config_file['application']['main_content']))
                    if final_data:
                        for json_obj in final_data:
                            if file_data:
                                json_obj['webpage_url'] = file_data['Url']
                            else:
                                json_obj['webpage_url'] = ''
                    if config_file['application']['elastic_dump']:
                        # check if the connection is established
                        if es.check_connection():
                            for data in final_data:
                                res = es.insert_data(data)
                                if res == 'created':
                                    pos_count = pos_count + 1
                                else:
                                    neg_count = neg_count + 1
                                print("Data Document inserted into Elasticsearch Successfully")
                        else:
                            print("Connection to Elasticsearch failed.")
                    with open(f'json_output_files/{os.path.splitext(FILES)[0]}.json', 'w+') as jsonfile_data:
                        json.dump(final_data, jsonfile_data, indent=4)
    if config_file['application']['elastic_dump']:
        print(f"{pos_count} insertion was successful \n\n {neg_count} insertion failed")
    return True

def search_key(json_obj, key):
    """
    Recursively search for a key in a JSON object and return its value
    """
    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            if k == key:
                return v
            else:
                result = search_key(v, key)
                if result is not None:
                    return result
    elif isinstance(json_obj, list):
        for item in json_obj:
            result = search_key(item, key)
            if result is not None:
                return result
    return None

