from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

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

print("full_url2:", full_url2)

''' +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ '''

# 학사안내 전체 페이지 수(2~583)
for i in range(0, min(30, int(data_number) // 10)):  # Adjusted the range limit to cover offset=290
    offset = (i + 1) * 10
    url = f"https://www.kumoh.ac.kr/ko/sub06_01_01_01.do?mode=list&articleLimit=10&article.offset={offset}"
    original_html = requests.get(url, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")

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

for index, url in enumerate(full_url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    board_contents = soup.find('div', class_='board-contents')
    
    if board_contents:
        text_content = board_contents.get_text(separator='\n', strip=True)

        # 파일 이름을 index를 기반으로 생성
        file_name = f"output_file_{index + 1}.txt"

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f"{url}에서 가져온 내용:\n{text_content}\n\n")

        print(f"{url}에서 가져온 내용을 {file_name}에 저장했습니다.")
    
    else:
        print(f"{url}에서 board-contents를 찾을 수 없습니다.")
