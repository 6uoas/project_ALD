import streamlit as st
import requests
from bs4 import BeautifulSoup

# 웹의 제목 설정
st.set_page_config(page_title="알라딘 최저가 탐색기")

# 페이지의 배경 이미지 설정
st.markdown(
    """
    <style>
    .title-container {
        background-image: url('https://pbs.twimg.com/media/BuzKgOoIcAAHYNa?format=jpg&name=small'); /* 배경 이미지 URL */
        background-size: cover; /* 배경 이미지를 컨테이너에 맞게 조정 */
        background-position: center; /* 배경 이미지 중앙 정렬 */
        padding: 40px; /* 패딩을 추가하여 제목과 배경 간의 간격 설정 */
        border-radius: 10px; /* 둥근 모서리 추가 */
        color: white; /* 제목 색상 설정 */
        text-align: center; /* 텍스트 중앙 정렬 */
    }
    </style>
    <div class="title-container">
        <h1>알라딘 최저가 탐색기</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 세션 상태 초기화
if 'isbn_list' not in st.session_state:
    st.session_state.isbn_list = []
    st.session_state.isbn_title = dict()

# ISBN 추가 함수
def add_isbn():
    isbn_input = st.session_state.isbn_input.strip()  # 앞뒤 공백 제거
    if isbn_input.replace(" ", "").isdigit():  # ISBN이 숫자만 이루어져 있는지 확인 (사이 공백 무시)
        isbn_input = isbn_input.replace(" ", "")  # ISBN에서 모든 공백 제거
        if isbn_input and isbn_input not in st.session_state.isbn_list:
            st.session_state.isbn_list.append(isbn_input)
            st.success(f"ISBN '{isbn_input}'가 추가되었습니다.")
            st.session_state.isbn_input = ""  # 입력란 초기화
        elif isbn_input in st.session_state.isbn_list:
            st.warning("이미 추가된 ISBN입니다.")
    else:
        st.warning("ISBN은 숫자만 입력해 주세요.")

# ISBN으로 제목 찾아주는 함수
def isbn_to_title(isbn):
    if isbn in st.session_state.isbn_title: #dp!
        return st.session_state.isbn_title[isbn]
    
    # ISBN에 따라 알라딘의 책 검색 URL 구성
    url = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord={isbn}"
    
    try:
        # HTTP GET 요청
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
        
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 책 제목 추출
        title_element = soup.find('a', class_='bo3')
        if title_element:
            title = title_element.find('b').text.strip()
            if title == '목차에서 검색':
                title = ':red[검색 결과가 없습니다. 삭제하고 다시 입력하세요]'
                st.session_state.isbn_title[isbn] = title
                return title
            st.session_state.isbn_title[isbn] = title
            return title
        else:
            title = ':red[검색 결과가 없습니다. 삭제하고 다시 입력하세요]'
            st.session_state.isbn_title[isbn] = title
            return title
    
    except requests.RequestException as e:
        return f"HTTP 요청 중 오류 발생: {e}"


# ISBN 입력
isbn_input = st.text_input("", placeholder="ISBN을 입력하고 엔터를 누르세요",
                            key="isbn_input", on_change=add_isbn)

# # 추가하기 버튼
# if st.button("추가하기"):
#     add_isbn()

# ISBN 목록 표시
st.subheader("추가된 책 목록",divider=True)
if st.session_state.isbn_list:
    for index, isbn in enumerate(st.session_state.isbn_list, start=1):
        col1, col2 = st.columns([9, 1])
        with col1:
            st.write(f"{index}. ISBN = {isbn}, *{isbn_to_title(isbn)}*")  # 넘버링 추가
        with col2:
            if st.button("삭제", key=isbn):
                st.session_state.isbn_list.remove(isbn)
                st.success(f"ISBN '{isbn}'가 삭제되었습니다.")
                st.rerun()  # 삭제 후 즉시 페이지를 다시 로드
    st.divider()

import func
every = dict()
isbns = []

# 최저가 탐색 버튼
if st.button("최저가 탐색"):
    if st.session_state.isbn_list:
        st.success("최저가 탐색을 시작합니다...")
        for isbn in st.session_state.isbn_list:
            tmp = func.dict_maker(isbn)
            every[isbn] = tmp
        
        best_combo = func.find_all_combinations(every)[1:]
        min_total_cost = func.find_all_combinations(every)[0]

        for i in range(len(best_combo)):
            if best_combo[i] != '품절된 책':
                st.write(f"ISBN-{st.session_state.isbn_list[i]}, {isbn_to_title(st.session_state.isbn_list[i])}")
                st.write(f"{best_combo[i]}에서 {every[st.session_state.isbn_list[i]][best_combo[i]]}원에 구매")
                st.divider()
            else:
                st.write(f"ISBN-{st.session_state.isbn_list[i]}, {isbn_to_title(st.session_state.isbn_list[i])}")
                st.write('재고 없음')
                st.divider()

        st.subheader(f"{min_total_cost}원")
    else:
        st.warning("ISBN 목록이 비어 있습니다. 먼저 ISBN을 추가해 주세요.")
