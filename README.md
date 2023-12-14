# KIT_kakao_AI_Project
Project of the Department of Artificial Intelligence Engineering at Kumoh National Institute of Technology


<br/>

# 역할 분배

## 😋 남현승

- 학교 홈페이지 파일 크롤링
- 공지사항 이미지 OCR
- 홈페이지 텍스트 크롤링
- 다운로드 받은 파일 텍스트 파일로 변환
- LLM 서치

## 😎 문지윤

- 카카오톡 채널 개설
- 카카오톡 스킬&블록 설정
- 네이버 서버 구축
- 서버 웹 구축(flask)
- 엘라스틱서치 코드 작성
- 카카오톡 챗봇, 네이버 서버, 엘라스틱서치, 챗GPT 연결


## shout out 윤신웅 

- openAI API 키 제공


<br/>

# 깃허브 디렉토리 설명

## 😄Crawling


### DOCX_TXT
  

: 구글문서 > txt 변환


<br/>


### HWP_TXT
   

: 한글hwp파일 > txt 변환


<br/>

### NOFI_OCR6
    

: 공지사항 이미지 OCR


<br/>
    

### NOFI_PDF
    

: 공지사항 첨부파일(pdf, hwp, docx ...) 다운로드


<br/>
    

### NOFI_TXT
    

: 공지사항 텍스트 크롤링
    

<br/>


<br/>


<br/>

## 😖 data

### project_data

    

: 공지사항 OCR, 첨부파일 데이터


<br/>
    

### school_text

    
: 3주차 과제 데이터


<br/>
   

### txt


: 공지사항 텍스트 데이터
    
<br/>


<br/>

<br/>

## 🤩 main


### app
    

: 서버 실행 코드(elasticsearch & chatGPT & kakao chatbot 연결)


<br/>
    

### es_delete
    

: es 색인화 삭제 코드


<br/>
    

### my_es
    

: es 색인화 코드
    