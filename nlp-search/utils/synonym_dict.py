import json
import sys
from configparser import ConfigParser
sys.path.insert(0,'/path/to/mod_directory')

config = ConfigParser()
config.read('.env')
base_url = config.get('application', 'base_url')

def json_data(path):
    dict_data = {}
    file_data = open(path,'r',encoding='utf-8').read().splitlines()
    for row_data in file_data:
        row_list = row_data.split(':')
        key_data = row_list[0]
        value_data = row_list[1].strip().split('|')
        dict_data[key_data] = value_data
    return dict_data

def intent_response_data(path):
    dict_data = {}
    file_data = open(path,'r').read().splitlines()
    for row_data in file_data:
        row_list = row_data.split(':')
        key_data = row_list[0]
        value_data = row_list[1].strip()
        dict_data[key_data] = value_data
    return dict_data

def append_base_url(data):
    if data:
        if base_url:
            if data['url']:
                data['url'] = base_url + data['url']
            if data['img']:
                data['img'] = base_url + data['img']
    
    return data
    
#example usage
# data = json_data('data/synonyms.txt')
# print(len(data))
#print(json.dumps(data,indent=3))