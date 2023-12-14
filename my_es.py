try:
  import os
  import elasticsearch
  from elasticsearch import Elasticsearch
  import numpy as np
  import pandas as pd
  import sys
  import json
  import time
  from ast import literal_eval
  from tqdm import tqdm
  import datetime
  from elasticsearch import helpers
  from langchain.text_splitter import CharacterTextSplitter


except Exception as e:
  print(f"error: {e}")


es = Elasticsearch(hosts = [{"host":"localhost", "port":9200,'scheme':'http'}])
# Check if python is connected to elasticsearch
print(es.ping())
# true

# Elasticsearch 인덱스 생성
index_name = 'txt_data_index'
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)


# 읽어올 디렉토리 경로들 설정
# directory_paths = os.getcwd()
directory_paths = ['<경로>',
                   '<경로>',
                   '<경로>']

# text_splitter 초기화
text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=50) # 청크 수 조절


# 각 디렉토리에 대해 작업 수행
for dir_index, directory_path in enumerate(directory_paths, start=1):
    # 디렉토리 내의 모든 파일 및 디렉토리 리스트
    files_and_dirs = os.listdir(directory_path)

    # 각 파일을 확인하여 txt 파일인 경우에만 읽어오기
    for item in tqdm(files_and_dirs, desc="파일 처리 중", unit="개"):
        item_path = os.path.join(directory_path, item)

        # 파일인지 확인
        if os.path.isfile(item_path):
            with open(item_path, 'r', encoding='utf-8') as file:
                data = file.read()
                text = data.replace('\n\n\n', ' ')
                
            # text_splitter를 사용하여 텍스트 분리
            chunks = text_splitter.split_text(text)

            # 데이터를 Elasticsearch에 색인화
            for j, chunk in enumerate(chunks, start=1):
                document = {
                    'text': chunk.strip(),  # 각 줄의 텍스트를 'text' 필드에 저장
                    'file_name': item,  # 파일 이름도 저장
                    'dir_index': dir_index,
                    'chunk_index': j
                }
                es.index(index=index_name, body=document)


# 색인화가 완료되었다면 몇 초 기다려서 Elasticsearch에 적용되도록 합시다.
time.sleep(5)


"""

# 특정 쿼리로 검색하기
search_query = '학생지원팀 전화번호?' # 여기 입력
search_body = {
    'query': {
        'match': {
            'text': search_query
        }
    },
    'size': 5 # 최대 5개의 문서만 반환(토큰 4000제한 때문에)
}

# 검색 실행
results = es.search(index=index_name, body=search_body)

# 결과 출력
print(f"검색어 '{search_query}'에 대한 검색 결과:")
for hit in results['hits']['hits']:
    print(hit['_source']['text'])

"""