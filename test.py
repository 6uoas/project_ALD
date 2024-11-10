class MyCustomException(Exception): #예외 클래스
    pass

def dict_maker(isbn) -> dict:

  from bs4 import BeautifulSoup
  from urllib.request import urlopen
  from urllib.error import HTTPError

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
    raise print(e)

  bs0bj = BeautifulSoup(html.read(),'html.parser') #html 전체 저장해놓고 있군..

  try:
    bo_used = bs0bj.findAll("a",{"class":"bo_used"}) #eBook 같은 것 찾아줌
  except AttributeError as e:
    raise print(e)
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



import time
start_time = time.time()

every = dict()
isbns = []


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

#9791168473690
#9788954699075
#9791167740984

print()

for i in every:
  print(f"ISBN: {i}")
  print(every[i])
  print()