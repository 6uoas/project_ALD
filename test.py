import requests
from bs4 import BeautifulSoup

def fetch_book_title(isbn):
    # ISBN에 따라 알라딘의 책 검색 URL 구성
    url = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord={isbn}&x=0&y=0"
    
    try:
        # HTTP GET 요청
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
        
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 책 제목 추출 (알라딘의 HTML 구조에 따라 다를 수 있음)
        title_element = soup.find('a', class_='bo3')
        if title_element:
            title = title_element.find('b').text.strip()
            return title
        else:
            return "책 제목을 찾을 수 없습니다."
    
    except requests.RequestException as e:
        return f"HTTP 요청 중 오류 발생: {e}"

# 예시 ISBN
isbn_input = "9791130649672"  # 여기에 실제 ISBN을 입력하세요
book_title = fetch_book_title(isbn_input)
print(f"ISBN: {isbn_input}의 책 제목은 '{book_title}'입니다.")
