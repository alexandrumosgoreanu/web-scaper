import json 
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import FunctionScore
INDEX_NAME = 'website_data'
ELASTIC_URL = 'http://localhost:9200'

f = open('data_best.json')

def connect_to_elastic():   
    try:
        es = Elasticsearch(ELASTIC_URL, verify_certs=False)
    except Exception as e:
        print(e)
    print('Connected to elastic')
    return es

def query_company_data(es, item):
    query_list = []
    if item['input_name']:
        query_list.append(Q('match', company_all_available_names = item['input_name']))

        # Splitting the input name and search for wildcards inside the social media link and the domain url
        input_name_strings = item['input_name'].split(' ')
        for string in input_name_strings:
            wildcard = '*' + ''.join(i for i in string.lower() if i.isalpha()) + '*'
            if wildcard != '**':
                wildcard_query = Q('wildcard', domain = wildcard)
                function_score = FunctionScore(query = wildcard_query, boost = 5.0)     # boosting wildcard matches in domain
                query_list.append(function_score)
                query_list.append(Q('wildcard', social_media = wildcard))

    if item['input_phone']:
        query_list.append(Q('match', phone = item['input_phone']))
    if item['input_website']:
        query_list.append(Q('match', domain = item['input_website'].replace('https', '').replace('http', '').replace(':', '').replace('//', '').replace('www.', '').split('/', 1)[0]))  # extracting only domain url
    if item['input_facebook']:
        query_list.append(Q('match', social_media = item['input_facebook']))

    query = Search(using=es, index='website_data').query(Q('bool', should = query_list,  minimum_should_match=1))
    # query = query[:1]                                        
    response = query.execute()
    return response
