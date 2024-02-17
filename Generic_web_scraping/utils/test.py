from elastic_data_dump import ElasticSearchClient
import json
import sys
import os


sys.path.insert(0, '/path/to/mod_directory')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

host = 'localhost'
port = 9200
index = 'test_aadya_indian_bank_db'


def insert_data(final_data):
    es = ElasticSearchClient(host,port,index,'_doc')
    # check if the connection is established
    if es.check_connection():
        print("Connection to Elasticsearch is established.")
        for data in final_data:
            res = es.insert_data(data)
        return "Success"    
    return "Connection to Elasticsearch failed."

#example usage

with open('json_output_files/indianbank_250.json', 'r') as f:
    data = json.load(f)
print(insert_data(data))
