
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


  try:
    result_count = bs0bj.find('span',{'class':'ss_f_g_l'})
    if result_count == None:
      raise MyCustomException("검색결과 없음 --> ISBN 다시 확인")
    elif int(''.join(result_count.get_text().split(','))) >= 10:
      raise MyCustomException("검색결과 많음 (동일 isbn이 10권 이상) --> ISBN 다시 확인")
  except AttributeError as e:
    print(e)

  try:
    bo_used = bs0bj.findAll("a",{"class":"bo_used"}) #<a class="bo_used" href="~~">eBook</a> 같은 것 찾아줌
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
      try: #직배송 중고 있으면
        store_price['직배송'] = min(tmp_price[i],store_price['직배송'])
      except: #직배송 중고 없으면
        store_price['직배송'] = tmp_price[i]

  #타입에 물건이 없으면 <span class='bo_used'~~>로 바뀜
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

  #절판인데 알라딘 직배송 중고가 없다면
  try:
    if store_price['직배송']==100000000:
      del store_price['직배송']
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
  '''
  for final_combo in best_combo:
    result.append(final_combo)
  '''
  return result



import time
start_time = time.time()

every = dict()
isbns = []

'''
test_data
for k in [9791191891287,9791192579504,9791156641131,9791162241639,9788968484698,9788996991342]:
  pass
'''

while True:

  try:
    isbn = input('ISBN 하나씩 입력 (종료하려면 q를 입력) : ').strip()
    if isbn in every:
      raise MyCustomException('이미 입력한 ISBN') #중복입력 방지
  except MyCustomException as e:
    print(e) # "이미 입력한 ISBN"
    print()
    continue

  i = time.time()

  if isbn =='q' or isbn =='Q':
    break
  else:
    print(f'searching for {isbn} in Aladin...')

    try:
      tmp = dict_maker(isbn)
    except MyCustomException as e: #문제있는 isbn의 경우
      print(e)
      print()
      continue
    except: #url이나 http문제의 경우
      print('url을 찾을 수 없음')
      print()
      continue

    every[isbn] = tmp
    isbns.append(isbn)

  f = time.time()
  print(f"{isbn} execution time : {f-i}s")
  print()

end_time = time.time()
print(f"total execution time : {end_time - start_time}s")

start_time = time.time()

best_combo = find_all_combinations(every)[1:]
min_total_cost = find_all_combinations(every)[0]

end_time = time.time()

# 최소 비용과 선택한 조합 출력
print('**가장 저렴한 조합**')

for i in range(len(best_combo)):
  if best_combo[i] != '품절된 책':
    print(f'ISBN : {isbns[i]} --> {best_combo[i]}에서 {every[isbns[i]][best_combo[i]]}원에 구매')
  else:
    print(f'ISBN : {isbns[i]} --> 재고 없음')

print(f'최종 최소 비용: {min_total_cost} 원')
print()
print(f'execution time : {end_time - start_time}s')


'''
data
voca = 9788965422785
vol4 rc = 9788917239508
vol4 lc = 9788917239492
vol3 rc = 9788917238549
vol3 lc = 9788917238532
vol2 rc = 9788917232196
vol2 lc = 9788917232189

'''