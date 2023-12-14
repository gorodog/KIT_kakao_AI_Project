import os
from docx import Document

def convert_all_docx_to_txt(input_folder, output_folder):
    # 폴더 내의 모든 파일 목록 가져오기
    files = os.listdir(input_folder)

    # .docx 파일만 선택하여 변환
    for file in files:
        if file.endswith(".docx"):
            docx_file_path = os.path.join(input_folder, file)
            # .txt 확장자로 변경하여 저장
            txt_file_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.txt')
            convert_docx_to_txt(docx_file_path, txt_file_path)

def convert_docx_to_txt(docx_path, txt_path):
    doc = Document(docx_path)
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for paragraph in doc.paragraphs:
            txt_file.write(paragraph.text + '\n')

# 사용 예시
input_folder_path = 'C:\\Users\\남현승\\Desktop\\programing\\PythonWorkspace\\kumoh\\Kakao\\docx'
output_folder_path = 'C:\\Users\\남현승\\Desktop\\programing\\PythonWorkspace\\kumoh\\Kakao\\docx'
convert_all_docx_to_txt(input_folder_path, output_folder_path)
