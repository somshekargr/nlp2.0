import json
import sys
import os
import traceback
from fastapi import HTTPException
import requests


def web_scrape():
    document = {}
    document['configurations'] = get_configurations("./config")

    try:
        process(document)
    except Exception:
        raise HTTPException(status_code=500, detail=get_error_details())
        
    return document

def read_config_files(filepath):
    print("from read-config_files {}".format(filepath))
    configurations = {}

    for (root, _, file_list) in os.walk(filepath):
        print("from read_config_file for loop 1")
        for file in file_list:
            print("from read_config_file for loop 2")
            filename = file.split('.')[0]
            if file.endswith('json') is False: continue

            try:
                print("from read_config_file try block")
                with open(root + '/' + file) as fd:
                    content = fd.read()
                    content = json.loads( content )
                    configurations[filename] = content
            except:
                print('UNEXPECTED ERROR :: ', sys.exc_info()[0])
                print('FILENAME :: {}'.format(file))
                sys.exit()

    # print(json.dumps(configurations, indent=4))
    return configurations

def get_configurations(filepath):
    return read_config_files(filepath)

def process(document):

    service = document['configurations']['service'] 

    # document['incoming-request']['incoming-request']['MESSAGE']['USER_NAME'] = 'Sopar Marpaung'

    document['result'] = []

    request = {
        "url"  : "https://www.indianbank.in/",
        "toZip"   : False
    }
   
    get_site_map_response = get_site_map(request=request, url=service['get-site-map'])
    log(topic='get-site-map', logging_data=get_site_map_response)

    html_dump_response = get_html_dumps(request=get_site_map_response, url=service['get-html-dumps'])
    log(topic='get-html-dumps', logging_data=html_dump_response)

    classifcation_response = classify_dump(request=html_dump_response, url=service['classify-dump'])
    log(topic='classify_dump', logging_data=classifcation_response)
    
    generate_and_insert_response = generate_and_insert(request=classifcation_response, url=service['generate-and-insert'])
    log(topic='generate-and-insert', logging_data=generate_and_insert_response)
    
    if generate_and_insert_response :
        document['result'] = generate_and_insert_response
    

    return document

def get_site_map(request, url):
    response = communicate(url, request)

    return response

def get_html_dumps(request, url):

    response = communicate(url, request)

    return response

def classify_dump(request, url):

    response = communicate(url, request)

    return response

def generate_and_insert(request, url):

    response = communicate(url, request)

    return response

def communicate(url, message):
    print("communicate : {} , {} ".format(url, message))
    message = json.dumps(message)
    result = requests.post(url, data=message).text
    
    result = json.loads(result)

    return result

def log(topic, logging_data):
    print('< [{}] {}\n'.format(topic, json.dumps(logging_data, indent=4)))
    
def get_error_details():
    ex_type, ex_value, ex_traceback = sys.exc_info()

    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)

    # Format stacktrace
    stack_trace = list()

    for trace in trace_back:
        stack_trace.append(f"File: {trace[0]}, Line: {trace[1]}, Func.Name: {trace[2]}, Message: {trace[3]}")

    return {
        'error_type': str(ex_type),
        'error_message': ex_value,
        'stacktrace': "\n".join(stack_trace)
    }
