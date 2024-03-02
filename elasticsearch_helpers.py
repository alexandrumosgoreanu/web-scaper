import json 
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

INDEX_NAME = "website_data"
ELASTIC_URL = "http://localhost:9200"

f = open('data_best.json')
scraped_results = json.load(f)

# json_file = json.dumps(scraped_results)
# with open("sample.json", "w") as outfile: 
#     outfile.write(json_file)
def connect_to_elastic():   
    try:
        es = Elasticsearch(ELASTIC_URL, verify_certs=False)
    except Exception as e:
        print(e)
    print('Connected to elastic')
    return es

i=0
def write_to_elastic(data):
    for item in data:
        index_result = es.index(index=INDEX_NAME, id=item['domain'], body=item)
        print(f"{i} : {index_result}")
        i+=1