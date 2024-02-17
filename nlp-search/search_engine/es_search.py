import os
import sys
import json
from configparser import ConfigParser

from utils.synonym_dict import json_data,intent_response_data
from utils.intent_search import search_dictionary, get_value_from_dictionary, search_dict_by_value,search_key_by_value
from utils.output import convert_to_json
from search_engine.es_class import Elastic, ElasticConfig
from search_engine.autocorrect_engine import w_autocorrect

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


config = ConfigParser()
config.read('.env')
es_host = config.get('elasticsearch_details', 'host')
es_port = int(config.get('elasticsearch_details', 'port'))
es_user = config.get('elasticsearch_details', 'user')
es_pass = config.get('elasticsearch_details', 'password')
es_index = config.get('elasticsearch_details', 'index')
website_search_intent_data = json_data(config.get('application', 'ws_intent_file_path'))
smalltalks_intent_data = json_data(config.get('application', 'smalltalks_intent_file_path'))
smalltalks_intent_response = intent_response_data(config.get('application', 'smalltalks_response_file_path'))
workflow_menu_intent_data = json_data(config.get('application', 'workflow_menu_intent_path'))
workflow_menu_intent_response = json.load(open(config.get('application', 'workflow_menu_response_path'),'r'))
none_response = config.get('application_response', 'none_response')

def es_data_search(user_query):
    
    es_config = ElasticConfig(es_host, es_port, es_user, es_pass)
    es_search_item = Elastic(es_config, es_index)
    
    auto_corrected_query = w_autocorrect(user_query.lower())
    print(auto_corrected_query)

    #_st_intent_value = search_dictionary(smalltalks_intent_data, auto_corrected_query.strip().lower())
    _st_intent_value = search_key_by_value(smalltalks_intent_data, auto_corrected_query.strip().lower())
    #print(temp_st_intent_value)

    if _st_intent_value is not None:
        bot_response = get_value_from_dictionary(smalltalks_intent_response,_st_intent_value)
        final_response = convert_to_json(user_query,auto_corrected_query.strip(),'smalltalks',bot_response)
        return final_response
    
    
    #smart_menu_intent = search_dictionary(workflow_menu_intent_data, auto_corrected_query.strip().lower())
    smart_menu_intent = search_key_by_value(workflow_menu_intent_data, auto_corrected_query.strip().lower())
    #print(temp_smart_menu_intent)
    if smart_menu_intent is not None:
        bot_response = search_dict_by_value(workflow_menu_intent_response,smart_menu_intent)
        final_response = convert_to_json(user_query,auto_corrected_query.strip(),'smartmenu',bot_response)
        return final_response
    
    _new_intent_value = search_dictionary(website_search_intent_data, auto_corrected_query.strip().lower())
    __new_intent_value = search_key_by_value(website_search_intent_data, auto_corrected_query.strip().lower())
    print(__new_intent_value)
    final_data = es_search_item.web_search(__new_intent_value, auto_corrected_query)
    if final_data != []:
        return convert_to_json(user_query,auto_corrected_query.strip(),'websitesearch',final_data)
    
    return convert_to_json(user_query,auto_corrected_query.strip(),'None',none_response)


def es_multichannel_data_search(user_query):
    
    es_config = ElasticConfig(es_host, es_port, es_user, es_pass)
    es_search_item = Elastic(es_config, es_index)
    
    auto_corrected_query = w_autocorrect(user_query.lower())
    print(auto_corrected_query)
    
    #_new_intent_value = search_dictionary(website_search_intent_data, auto_corrected_query.strip().lower())
    __new_intent_value = search_key_by_value(website_search_intent_data, auto_corrected_query.strip().lower())
    print(__new_intent_value)
    final_data = es_search_item.web_search(__new_intent_value, auto_corrected_query)
    if final_data != []:
        return convert_to_json(user_query,auto_corrected_query.strip(),'websitesearch',final_data)
    
    return convert_to_json(user_query,auto_corrected_query.strip(),'None',none_response)