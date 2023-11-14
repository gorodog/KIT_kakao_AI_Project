from bs4 import BeautifulSoup
import requests
import re



# ConnectionError방지
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102" }



''' +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ '''



# 총 자료 개수 가져오기
url = "https://www.kumoh.ac.kr/ko/sub06_01_01_01.do"
original_html = requests.get(url, headers=headers)
html = BeautifulSoup(original_html.text, "html.parser")

data_number = html.select("#jwxe_main_content > div.contents-wrapper > div.board-area.ko.board.list > form:nth-child(1) > fieldset > div > p > strong")



''' +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ '''



# url 저장 변수
get_url = []



# 1페이지 & 공지
url = "https://www.kumoh.ac.kr/ko/sub06_01_01_01.do?mode=list&&articleLimit=10&article.offset=0"
original_html = requests.get(url, headers=headers)
html = BeautifulSoup(original_html.text, "html.parser")

tbody = html.select_one('#jwxe_main_content > div.contents-wrapper > div.board-area.ko.board.list > div.board-list01 > table > tbody')

# tbody 내부의 모든 링크 추출하기
url_elements = tbody.find_all('a', href=True)

# 추출된 URL 저장
for element in url_elements:
    get_url(element['href']) # <a> 태그의 'href' 속성값 추출




# 학사안내 전체 페이지 수(2~583)
for i in range(1, data_number/10+1):
    url = f"https://www.kumoh.ac.kr/ko/sub06_01_01_01.do?mode=list&&articleLimit=10&article.offset={}00"
    original_html = requests.get(url, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    
    # 원하는 tbody 선택하기 (특정 클래스에 속한 경우)
    tr_elements = html.select('#jwxe_main_content > div.contents-wrapper > div.board-area.ko.board.list > div.board-list01 > table > tbody tr.')

    # tr 내부의 모든 링크 추출하기
    url_elements = [tr.find('a', href=True) for tr in tr_elements]

    # 추출된 URL 출력
    for element in url_elements:
        get_url(element['href'])



''' +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ '''



# 각 url에서 정보 추출
for i in range(1, data_number/10+1):
    url = get_url[i]
    original_html = requests.get(url, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    
    # 제목
    title_ = html.find('h3', class_='board-view-title')
    title = title_.get_text()
    
    # 텍스트 처리
    
    # 이미지 처리
    
    # 첨부 파일 처리
    
    # 각각 문서로 저장...?