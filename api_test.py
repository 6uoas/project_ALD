from bs4 import BeautifulSoup
import requests
import streamlit as st
import pandas as pd
import json

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

'''
try:
    html = urlopen("https://www.aladin.co.kr/home/welcome.aspx")
except HTTPError as e:
    print(e)
except URLError as e:
    print("알라딘 서버가 다운되었습니다.")
else:
    print("정상적으로 html을 가져왔습니다.")
'''


#key = ttbparktimothy260422001

key = ['ttbparktimothy260422001']
url = f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={key}&QueryType=ItemNewAll&MaxResults=100" \
      "&start=1&SearchTarget=Book&output=js&Version=20131101&CategoryId=50993"

#request 보내기
response = requests.get(url)

#받은 response를 json 타입으로 바뀌주기
response_json = json.loads(response.text)
#확인
print(response_json)

'''
print(bs.h1)

<h1><a href="https://www.aladin.co.kr/home/start.aspx"
id="logoBtn" title="알라딘 첫화면으로 가기">
<img alt="알라딘" src="//image.aladin.co.kr/img/header/2023/aladin_logo.jpg"/
</a>
</h1>
처음 확인되는 h1 태그 모두 반환
'''
