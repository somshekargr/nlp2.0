# import json
import sys
import os
from elasticsearch import Elasticsearch
from utils.synonym_dict import append_base_url
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class ElasticConfig:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password


class Elastic:
    def __init__(self, config, index):
        self.config = config
        self.index = index
        #self.faq_index =
        #self.e_s = Elasticsearch([{'host': self.config.host, 'port': self.config.port,"timeout":30, "max_retries":10, "retry_on_timeout":True}])
        
        self.e_s = Elasticsearch(
            [{'host': self.config.host, 'port': self.config.port, 'scheme': 'http'}],
            timeout=30,
            max_retries=10,
            retry_on_timeout=True,
            basic_auth=(self.config.user, self.config.password)
        )

    def web_search(self, intent, query):
        es_result = self.search_with_original_query(intent, query)
        if es_result is None:
            return []

        documents = self.extract_documents(es_result)
        return documents

    def search_with_original_query(self, intent, search_string):
        if intent:
            body = {
                "size": 10,
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"subject": intent}},
                        ]
                    }
                }
            }
            initial_results = self.e_s.search(index=self.index, body=body)
            relevant_ids = [hit["_id"]
                            for hit in initial_results["hits"]["hits"]]
            print(search_string)
            filter_query = {
                "size": 5,
                "query": {
                    "bool": {
                        "filter": {
                            "terms": {
                                "_id": relevant_ids
                            }
                        },
                        "should": [
                            {"match": {"subject_stem": intent}},
                            {"match": {"pedicate": search_string}},
                            {"match": {"extended_table": search_string}},
                            {"match": {"object": search_string}}
                        ]

                    }
                }
            }
            es_result = self.e_s.search(index=self.index, body=filter_query)
            # print(len(es_result['hits']['hits']))

        else:
            body = {
                "size": 5,
                "query": {
                    "bool": {
                        "should": [
                            {"match": {"subject": search_string}},
                            {"match": {"subject_stem": search_string}},
                            {"match": {"pedicate": search_string}},
                            {"match": {"extended_table": search_string}},
                            {"match": {"object": search_string}}
                        ]
                    }
                }
            }

            es_result = self.e_s.search(index=self.index, body=body)

        if len(es_result['hits']['hits']) == 0:
            return None

        return es_result

    def extract_documents(self, es_result):
        documents = []
        for record in es_result['hits']['hits']:
            source = record['_source']
            #if record['_score'] > 0:
            documents.append({
                'main_title': source['subject'],
                'url': source['webpage_url'],
                'score': record['_score'],
                'title': source['pedicate'],
                'stemmed_title': source['pedicate_stem'],
                'value': source['object'],
                'extended_value': source['extended_table'],
                'additional_data': append_base_url(source['additional_data'])
            })
        return documents
