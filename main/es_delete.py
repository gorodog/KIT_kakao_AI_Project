from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{"host": "localhost", "port": 9200, 'scheme': 'http'}])
# es = Elasticsearch(['http://localhost:9200'])

# 삭제할 색인 이름 지정
index_name = "txt_data_index"

# 색인이 존재하는지 확인 후 삭제
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"색인 '{index_name}'이 삭제되었습니다.")
else:
    print(f"색인 '{index_name}'이 이미 존재하지 않습니다.")