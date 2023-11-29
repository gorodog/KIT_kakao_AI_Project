from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os
from io import BytesIO
from PIL import Image
from easyocr import Reader

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

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
for i in range(0, min(30, int(data_number) // 10)):
    offset = i * 10  # 수정된 부분
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

print("full_url:", full_url)

def download_images(image_urls, output_directory, site_index):
    for url in image_urls:
        response = requests.get(url)
        
        if response.status_code == 200 and response.headers['Content-Type'].startswith('image'):
            try:
                img = Image.open(BytesIO(response.content))
                img.save(os.path.join(output_directory, f"image_{site_index}_{image_urls.index(url)}.png"))
            except Exception as e:
                print(f"{url}에서 이미지 처리 중 오류 발생: {e}")
        else:
            print(f"{url}에서 이미지 다운로드 실패. 상태 코드: {response.status_code}")
          
""" +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ """

def extract_text_from_image(image_path):
    reader = Reader(['ko'])
    result = reader.readtext(image_path)
    return result

def get_image_urls(website_url):
    response = requests.get(website_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        
        # Use urljoin to handle incomplete URLs
        base_url = response.url
        image_urls = [urljoin(base_url, img['src']) for img in img_tags if 'src' in img.attrs]
        return image_urls
    else:
        print(f"Failed to fetch {website_url}. Status code: {response.status_code}")
        return []

""" +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ """

output_directory = 'downloaded_images'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

site_texts = {}

for i, url in enumerate(full_url):
    image_urls = get_image_urls(url)

    download_images(image_urls, output_directory, i)

for i, url in enumerate(full_url):
    site_texts[i] = []

    for filename in os.listdir(output_directory):
        if filename.startswith(f"image_{i}_") and filename.endswith(".png"):
            image_path = os.path.join(output_directory, filename)
            text_results = extract_text_from_image(image_path)

            if text_results:
                for text_result in text_results:
                    site_texts[i].append(text_result[1])  # Store the extracted text

                print(f"Text extracted from {filename}:")
                for text_result in text_results:
                    print(text_result[1])
            else:
                # Remove the image file if no text is found
                os.remove(image_path)

""" +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ """
                
for site_index, texts in site_texts.items():
    seen_images = set()  # To store unique images seen so far
    duplicate_images = set()  # To store duplicate images

    for i, text in enumerate(texts):
        image_path = os.path.join(output_directory, f"image_{site_index}_{i}.png")
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()

        if img_data in seen_images:
            duplicate_images.add(image_path)
        else:
            seen_images.add(img_data)

    for redundant_image_path in duplicate_images:
        if os.path.exists(redundant_image_path):
            os.remove(redundant_image_path)

""" +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ """

for site_index, texts in site_texts.items():
    for i, text in enumerate(texts):
        image_path = os.path.join(output_directory, f"image_{site_index}_{i}.png")
        if os.path.exists(image_path):
            print(f"Text extracted from {image_path}:")
            print(text)
