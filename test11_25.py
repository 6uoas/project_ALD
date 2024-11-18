import streamlit as st
import requests
from bs4 import BeautifulSoup

# 웹의 제목 설정
st.set_page_config(page_title="알라딘 중고 최저가 탐색기")

from urllib.error import HTTPError

class MyCustomException(Exception): #예외 클래스
    pass

#isbn 입력시 알라딘에서 구매 가능한 모든 새책, 중고책 딕셔너리 반환
def dict_maker(isbn) -> dict:

  from bs4 import BeautifulSoup
  from urllib.request import urlopen

  tmp_url = ("https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Used&KeyWord=" +
            isbn +
            "&KeyRecentPublish=0&OutStock=0&ViewType=Detail&CustReviewCount=0&CustReviewRank=0&KeyFullWord=" +
            isbn +
            "&KeyLastWord=" +
            isbn +
            "&CategorySearch=&chkKeyTitle=&chkKeyAuthor=&chkKeyPublisher=&chkKeyISBN=&chkKeyTag=&chkKeyTOC=&chkKeySubject=&SuggestKeyWord="
            )

  try: #HTTPError 예외처리
    html = urlopen(tmp_url)
  except HTTPError as e:
    raise MyCustomException(e)

  bs0bj = BeautifulSoup(html.read(),'html.parser') #html 전체 저장해놓고 있군..


  # try:
  #   result_count = bs0bj.find('span',{'class':'ss_f_g_l'})
  #   if result_count == None:
  #     raise MyCustomException("검색결과 없음 --> ISBN 다시 확인")
  #   elif int(''.join(result_count.get_text().split(','))) >= 10:
  #     raise MyCustomException("검색결과 많음 (동일 isbn이 10권 이상) --> ISBN 다시 확인")
  # except AttributeError as e:
  #   print(e)

  try:
    bo_used = bs0bj.findAll("a",{"class":"bo_used"}) #eBook 같은 것 찾아줌
  except AttributeError as e:
    raise MyCustomException(e)
  tmp_type, tmp_price, store_price =[], [], {}
  used_store_html = []

  for i in bo_used:
    if '원' in i.get_text(): # get_text하면 eBook만 출력함
      try:
        tmp_price.append(int(''.join(i.get_text()[:-1].split(','))))
      except: #절판인 경우 엄두도 못낼 가격으로 배제
        tmp_price.append(100000000) #중고가 있을 수 있어서 예외처리
    else:
      tmp_type.append(i.get_text())
    if '우주점' in i.get_text():
      used_store_html.append('https://www.aladin.co.kr' + i.attrs['href'])

  for i in range(len(tmp_type)):
    if tmp_type[i]=='새책' or '알라딘' in tmp_type[i]:
      try: #알라딘 중고 있으면
        store_price['알라딘'] = min(tmp_price[i],store_price['알라딘'])
      except: #알라딘 중고 없으면
        store_price['알라딘'] = tmp_price[i]

  #타입에 물건이 없으면 로 바뀜
  if used_store_html != []:
    for i in used_store_html:
      html = urlopen(i)
      bs0bj = BeautifulSoup(html.read(),'html.parser')
      price = bs0bj.findAll('span',{"class":"Ere_fs20 Ere_sub_pink"}) #가격 리스트를 전달 함
      seller = bs0bj.findAll('li',{"class":"Ere_store_name"}) # 매장 리스트를 전달함
      # findAll은 위에서부터 순서대로 찾아내서 같은 인덱스번호에 매장-가격 위치함

      for j in range(len(price)):
        for k in range(len(price)):
          if seller[k].get_text()[4:] not in store_price: #같은 매장에서는 최저가만
            store_price[seller[k].get_text()[4:]] = int(''.join(price[k].get_text().split(",")))

  #절판인데 알라딘 알라딘 중고가 없다면
  try:
    if store_price['알라딘']==100000000:
      del store_price['알라딘']
  except:
    pass

  #재고가 1도 없을 경우
  if store_price == {}:
    return {'품절된 책':0}
  else:
    return store_price

#dict_maker에서 반환한 isbn들을 모아 가능한 모든 조합 찾고 최저가인 조합 반환
def find_all_combinations(book_prices) -> list: #[0] : total_cost, [1:] : combo
  import itertools

  # 모든 가능한 책과 가게 조합 생성
  combinations = list(itertools.product(*[book_prices[book].keys() for book in book_prices]))

  # 초기 최소 비용을 무한대로 설정
  min_total_cost = float('inf')
  best_combo = None

  # 각 조합에 대한 최소 비용 계산
  for combo in combinations:

      #모든 가게에 대한 장바구니 준비
      store_dict = {store: 0 for prices in book_prices.values() for store in prices}
      total_cost = 0

      for i, book in enumerate(book_prices):
          store = combo[i]
          store_dict[store] += book_prices[book][store]

      # 한 가게에서 20000원 미만으로 구매할 때만 배송비 추가
      for store_tmp in store_dict:
        if store_tmp == '품절된 책': #품절된 책 예외처리
          pass
        else:
          if store_dict[store_tmp] == 0: #0원이 담긴 가게 예외처리
            pass
          elif store_dict[store_tmp] < 20000:
            total_cost += store_dict[store_tmp]
            total_cost += 2500 #배송비
          else:
            total_cost += store_dict[store_tmp]

      if total_cost < min_total_cost:
          min_total_cost = total_cost
          best_combo = combo

  result = [min_total_cost, *best_combo]

  return result

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
        <h1>알라딘 중고 최저가 탐색기</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 세션 상태 초기화
if 'isbn_list' not in st.session_state:
    st.session_state.isbn_list = [] # isbn담기는 곳
    st.session_state.isbn_title = dict() # isbn별 책 제목 담기는 곳

# ISBN 추가 함수
def add_isbn():
    isbn_input = st.session_state.isbn_input.strip()  # 앞뒤 공백 제거
    if isbn_input.replace(" ", "").isdigit():  # ISBN이 숫자만 이루어져 있는지 확인 (사이 공백 무시)
        isbn_input = isbn_input.replace(" ", "")  # ISBN에서 모든 공백 제거

        if len(isbn_input) != 13:
            st.warning("ISBN은 13자리 수로 이루어져 있습니다.")
        #elif isbn_input and isbn_input not in st.session_state.isbn_list:
        elif len(isbn_input) == 13 and isbn_input not in st.session_state.isbn_list:
            st.session_state.isbn_list.append(isbn_input)
            st.success(f"ISBN '{isbn_input}'가 추가되었습니다.")
            st.session_state.isbn_input = ""  # 입력란 초기화
        elif isbn_input in st.session_state.isbn_list:
            st.warning("이미 추가된 ISBN입니다.")
    else:
        st.warning("숫자만 입력해 주세요.")

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
            title = title_element.text.strip()
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
        return f":red[HTTP 요청 중 오류 발생:] {e}"

st.write("")
st.write("")

# ISBN 입력

# st.subheader("ISBN 입력", divider=True)
st.subheader("ISBN 입력")

isbn_input = st.text_input("", placeholder="ISBN을 입력하고 엔터를 누르세요",
                            key="isbn_input", on_change=add_isbn)

# 추가하기 버튼
if st.button("목록에 추가하기"):
    add_isbn()

st.write('')
st.write('')

# st.subheader("추가된 책 목록",divider=True)
st.subheader("추가된 책 목록")
# ISBN 목록 표시
if st.session_state.isbn_list:
    for index, isbn in enumerate(st.session_state.isbn_list, start=1):
        col1, col2 = st.columns([9, 1])
        with col1:
            st.write(f"{index}. ISBN-{isbn}, *{isbn_to_title(isbn)}*")  # 넘버링 추가
        with col2:
            if st.button("삭제", key=isbn):
                st.session_state.isbn_list.remove(isbn)
                st.success(f"ISBN '{isbn}'가 삭제되었습니다.")
                st.rerun()  # 삭제 후 즉시 페이지를 다시 로드
#    # 모두 삭제 버튼 추가
#    col3, col4 = st.columns([9,2])
#    with col3:
#        st.write('')
#    with col4:
#        if st.button("모두 삭제"):
#            st.session_state.isbn_list.clear()
#            st.success("모든 ISBN이 삭제되었습니다.")
#            st.rerun()
else:
    st.write("**:red[아직 추가된 책이 없습니다.]**")
    st.write("")

every = dict()
isbns = []

st.divider()
search = st.button("최저가 탐색")
st.write("")
st.write("")

# 최저가 탐색 버튼
if search:
    st.subheader('최저가 조합',divider=True)
    if st.session_state.isbn_list:
        #st.success("최저가 탐색을 시작합니다...")
        st.divider()
        for isbn in st.session_state.isbn_list:
            tmp = dict_maker(isbn)
            every[isbn] = tmp
        
        best_combo = find_all_combinations(every)[1:]
        min_total_cost = find_all_combinations(every)[0]

        for i in range(len(best_combo)):
            if best_combo[i] != '품절된 책':
                st.write(f"ISBN-{st.session_state.isbn_list[i]}, {isbn_to_title(st.session_state.isbn_list[i])}")
                st.write(f"{best_combo[i]}에서 {format(int(every[st.session_state.isbn_list[i]][best_combo[i]]),',d')}원에 구매")
                st.divider()
            else:
                st.write(f"ISBN-{st.session_state.isbn_list[i]}, {isbn_to_title(st.session_state.isbn_list[i])}")
                st.write('중고 재고 없음')
                st.divider()

        st.subheader(f"{format(int(min_total_cost),',d')}원")
    else:
        st.warning("ISBN 목록이 비어 있습니다. 먼저 ISBN을 추가해 주세요.")