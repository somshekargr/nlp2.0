from uuid import uuid1
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError


class ElasticSearchClient:
    def __init__(self, host, port, index, doc_type,username,password):
        self.host = host
        self.port = port
        self.index = index
        self.doc_type = doc_type
        self.user = username
        self.password = password
        self.es = Elasticsearch([
            {'host': self.host, 'port': self.port, 'scheme': 'http'}],
            timeout=30,
            max_retries=10,
            retry_on_timeout=True,
            basic_auth=(self.user,self.password))

    def check_connection(self):
        try:
            self.es.ping()
            return True
        except ConnectionError as e:
            print(f"Error connecting to Elasticsearch: {e}")
            return False

    def insert_data(self, data):
        try:
            res = self.es.index(index=self.index,
                          id=str(uuid1()), body=data)
            return res['result']
        except ConnectionError as e:
            print(f"Error inserting data into Elasticsearch: {e}")
            return None

    def delete_index(self):
        try:
            self.es.indices.delete(index=self.index, ignore=[400, 404])
            print("deleted es index {}".format(self.index))
            return True
        except Exception as e:
            print(f"Error deleting the index: {e}")
            return False