from flask import Flask, jsonify, request
import requests, sys, json
from elasticsearch import Elasticsearch

# 수정 작성 : <your_index_name>, <openAI API Key>, <Asyncia API Key>

es = Elasticsearch(['http://localhost:9200'])
# Check if python is connected to elasticsearch
print(es.ping())
# true

application = Flask(__name__)
a = {}



@application.route("/webhook/", methods=["POST"])
def webhook():
    global a
    request_data = json.loads(request.get_data(), encoding='utf-8')
    a[request_data['user']] = request_data['result']['choices'][0]['message']['content']
    return 'OK'



@application.route("/question", methods=["POST"])
def get_question():
    global a
    request_data = json.loads(request.get_data(), encoding='utf-8')

    question = request_data['action']['params']['question']

    a[request_data['userRequest']['user']['id']] = '아직 AI가 처리중이에요'

    # 검색할 인덱스와 쿼리 정의
    index_name = '<your_index_name>'
    search_body = {
        'query': {
            'match': {
                'text': question
            }
        },
        'size': 3 # 최대 3개의 문서만 반환
    }

    # 쿼리 실행
    response = es.search(index=index_name, body=search_body)

    # 결과 저장
    result_text = ""
    for hit in response['hits']['hits']:
        result_text += hit['_source']['text'] + "\n\n\n 다음문서:\n"
    r_text = result_text.replace('\n', ' ')
    r_r_text = r_text[:500] # 글자수 300자까지 자르기

    a[request_data['userRequest']['user']['id']] = r_r_text

    response = { "version": "2.0", "template": { "outputs": [{
        "simpleText": {"text": f"질문('{request_data['action']['params']['question']}')을 받았습니다.'답변'을 입력하시면 답변이 전송됩니다."}
    }]}}

    # try:
        # api = requests.post('https://api.asyncia.com/v1/api/request/', json={
            # "apikey": "<openAI API Key>",
            # "messages" :[{"role": "user", "content": r_text}],
            # "userdata": [["user", request_data['userRequest']['user']['id']]]},
            # headers={"apikey":"<Asyncia API Key>"}, timeout=0.3)
    # except requests.exceptions.ReadTimeout:
        # pass
    return jsonify(response)

@application.route("/ans", methods=["POST"])
def hello2():
    request_data = json.loads(request.get_data(), encoding='utf-8')
    response = { "version": "2.0", "template": { "outputs": [{
        "simpleText": {"text": f"답변: {a.get(request_data['userRequest']['user']['id'], '질문을 하신적이 없어보여요. 질문부터 해주세요')}"}
    }]}}
    return jsonify(response)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=3000, debug=True)
