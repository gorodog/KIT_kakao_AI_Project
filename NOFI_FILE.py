from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os
import re

# ConnectionError 방지
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

# url 저장 변수
get_url = []

base_url = "https://www.kumoh.ac.kr/ko/sub06_01_01_01.do"

''' +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ '''

# 총 자료 개수 가져오기
base_url = "https://www.kumoh.ac.kr/ko/sub06_01_01_01.do"
original_html = requests.get(base_url, headers=headers)
html = BeautifulSoup(original_html.text, "html.parser")

data_number = html.select_one("#jwxe_main_content > div.contents-wrapper > div.board-area.ko.board.list > form:nth-child(1) > fieldset > div > p > strong").get_text()

''' +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ '''

# 1페이지 & 공지
url = "https://www.kumoh.ac.kr/ko/sub06_01_01_01.do"
original_html = requests.get(url, headers=headers)
html = BeautifulSoup(original_html.text, "html.parser")

# tbody 내부의 모든 링크 추출하기
tbody = html.select_one('#jwxe_main_content > div.contents-wrapper > div.board-area.ko.board.list > div.board-list01 > table > tbody')

if tbody:
    url_elements = tbody.find_all('a', href=True)

    # 추출된 URL 저장
    for element in url_elements:
        get_url.append(element['href'])
else:
    print("tbody not found.")

print("get_url: ", get_url)

full_url2 = []

for url in get_url:
    full_url2.append(urljoin(base_url, url))


''' +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ '''

# 학사안내 전체 페이지 수(2~583)
for i in range(0, min(30, int(data_number) // 10)):
    offset = (i + 1) * 10  # 수정된 부분
    url = f"https://www.kumoh.ac.kr/ko/sub06_01_01_01.do?mode=list&articleLimit=10&article.offset={offset}"
    original_html = requests.get(url, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")  # 수정된 부분

    # 원하는 tbody 선택하기 (특정 클래스에 속한 경우)
    tr_elements = html.select('#jwxe_main_content > div.contents-wrapper > div.board-area.ko.board.list > div.board-list01 > table > tbody tr')

    # tr 내부의 모든 링크 추출하기
    url_elements = [tr.find('a', href=True) for tr in tr_elements]

    # 추출된 URL 저장
    for element in url_elements:
        get_url.append(element['href'])

""" +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ """

# 기본 URL과 상대 URL 조합
full_url = [urljoin(base_url, url) for url in get_url]

# clean_filename 함수 수정
def clean_filename(filename):
    # 특수문자 및 공백 제거
    cleaned_filename = re.sub(r'[\/:*?"<>|]', '', filename)
    # 사용할 수 없는 문자를 언더스코어로 대체
    cleaned_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', cleaned_filename)
    # 파일명이 너무 길면 잘라서 사용
    max_filename_length = 255  # 파일 시스템에 따라 제한이 있을 수 있음
    return cleaned_filename[:max_filename_length]

''' +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ '''

# PDF 및 HWP 다운로드 함수
def download_files(url, folder="."):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # PDF 및 HWP 파일 찾기
    file_links = []
    for a in soup.find_all('a', href=True):
        if 'file-down-btn' in a.get('class', []):
            file_links.append(a['href'])
    
    for i, file_link in enumerate(file_links, start=1):
        absolute_url = urljoin(url, file_link)
        file_response = requests.get(absolute_url, stream=True, headers=headers)
        
        # 파일명 추출 및 사용할 수 없는 문자 정제
        content_disposition = file_response.headers.get("Content-Disposition")
        filename = content_disposition.split("filename=")[1].strip('"') if content_disposition else f"file{i}.pdf"
        filename = clean_filename(filename)
        
        # 파일 저장
        os.makedirs(folder, exist_ok=True)  # 폴더가 없으면 생성
        with open(os.path.join(folder, filename), 'wb') as file:
            for chunk in file_response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded: {filename}")

''' +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ '''

# 각 링크에서 PDF 및 HWP 다운로드
for link in full_url:
    download_files(link, folder="file_downloads")
