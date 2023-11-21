import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO
from PIL import Image
from easyocr import Reader

# Function to download images from URLs
def download_images(image_urls, output_directory):
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.save(os.path.join(output_directory, f"image_{image_urls.index(url)}.png"))

# Function to extract text using EasyOCR
def extract_text_from_image(image_path):
    reader = Reader(['ko'])
    result = reader.readtext(image_path)
    return result

# Function to get image URLs from a website
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

# Main function
def main():
    website_url = 'https://www.kumoh.ac.kr/ko/sub06_01_01_01.do?mode=view&articleNo=469183&article.offset=0&articleLimit=10'
    output_directory = 'downloaded_images'

    # Create the directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get image URLs from the website
    image_urls = get_image_urls(website_url)

    # Download images to the specified directory
    download_images(image_urls, output_directory)

    # Perform OCR on each downloaded image and print the extracted text
    for filename in os.listdir(output_directory):
        if filename.endswith(".png"):
            image_path = os.path.join(output_directory, filename)
            text_results = extract_text_from_image(image_path)

            # Check if there is any text extracted
            if text_results:
                print(f"Text extracted from {filename}:")
                for text_result in text_results:
                    print(text_result[1])  # Print the extracted text to the console
            else:
                # Remove the image file if no text is found
                os.remove(image_path)

if __name__ == "__main__":
    main()
