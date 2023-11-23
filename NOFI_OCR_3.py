from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os
from io import BytesIO
from PIL import Image
from easyocr import Reader

# ConnectionError 방지
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

# url 저장 변수
get_url = []

base_url = "https://www.kumoh.ac.kr/ko/sub06_01_01_01.do"

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

full_url2 = []

for url in get_url:
    full_url2.append(urljoin(base_url, url))

print("full_url2:", full_url2)

''' +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ '''

# URL 이미지 다운로드 함수수
def download_images(image_urls, output_directory, site_index):
    for url in image_urls:
        response = requests.get(url)
        
        # 응답이 성공하고 이미지 유형인지 확인
        if response.status_code == 200 and response.headers['Content-Type'].startswith('image'):
            try:
                img = Image.open(BytesIO(response.content))
                img.save(os.path.join(output_directory, f"image_{site_index}_{image_urls.index(url)}.png"))
            except Exception as e:
                print(f"{url}에서 이미지 처리 중 오류 발생: {e}")
        else:
            print(f"{url}에서 이미지 다운로드 실패. 상태 코드: {response.status_code}")


# EasyOcr 함수
def extract_text_from_image(image_path):
    reader = Reader(['ko'])
    result = reader.readtext(image_path)
    return result

# 웹사이트에서 URL에 이미지 가져오기기
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

# 메인 함수
output_directory = 'downloaded_images'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for i, url in enumerate(full_url2):
    image_urls = get_image_urls(url)

    # 디렉토리에 이미지 다운
    download_images(image_urls, output_directory, i)

    # 다운로드한 각 이미지에 대해 OCR 수행
    for filename in os.listdir(output_directory):
        if filename.endswith(".png"):
            image_path = os.path.join(output_directory, filename)
            text_results = extract_text_from_image(image_path)

            if text_results:
                print(f"Text extracted from {filename}:")
                for text_result in text_results:
                    print(text_result[1])  # Print the extracted text to the console
            else:
                # Remove the image file if no text is found
                os.remove(image_path)
