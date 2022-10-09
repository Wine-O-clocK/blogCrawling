from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter
from difflib import get_close_matches
from datetime import datetime
from dateutil.relativedelta import relativedelta
from konlpy.tag import Okt
from konlpy.tag import Kkma
from nltk import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import pandas as pd
import numpy as np
import time
import math
import nltk

okt = Okt()
kkma = Kkma()
#nltk.download()
sia = SentimentIntensityAnalyzer()

path = 'C:/Users/limga/OneDrive/Desktop/data/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(path)

now = str(datetime.now().date())
before_one_month = str((datetime.now() - relativedelta(months=1)).date())

url_list = []
content_list = ''
text = '와인 입문자 추천'
result = []

# 페이지 범위 정함
url = 'https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=MONTH&orderBy=sim&startDate=' + before_one_month + '&endDate=' + now + '&keyword=' + text
driver.get(url)
cnt = int(driver.find_element(By.XPATH, '/html/body/ui-view/div/main/div/div/section/div[1]/div[2]/span/span/em').text[:-1])
page = math.trunc(cnt/7)+1

# 크롤링 한 와인 정보들
wine_list = pd.read_csv('wine_list.csv', encoding='utf-8')
subset = wine_list['이름']
wine_data = np.array(subset.tolist()) 

def get_count(content):
	wine_result = []  # 와인 count 결과
  	# wine 배열 돌면서 블로그 내용에 해당 와인 있는지 확인 (있다면 wine_result에 추가)
	# replace 사용하여 공백 제거 후 확인
	for w in wine_data:
		val = content_list.replace(" ", "").find(w.replace(" ", ""))
		if (val == -1): continue
		else: 
			if w not in wine_result: wine_result.append(w)
			else: continue
	return wine_result

def get_taste(nouns):
	return '맛' in nouns and '입맛' not in nouns and '맛집' not in nouns and len(nouns) > 1

def get_access(nouns):
	return '편의점' in nouns or '이마트' in nouns or '홈플러스' in nouns \
    	or '롯데마트' in nouns or '코스트코' in nouns or '트레이더스' in nouns or '홈술' in nouns \
    	or '씨유' in nouns or 'CU' in nouns or 'gs25' in nouns or '세븐일레븐' in nouns or '미니스톱' in nouns

def get_present(nouns):
	return '선물' in nouns

# 감정 분석 평균 구하기
def get_average(score):
	neg=[]  # 부정
	neu=[]  # 긍정
	result = 1
	if len(score) > 0:
		for s in score:
			neg.append(s['neg'])
			neu.append(s['neu'])
			neg_aver = np.mean(neg)
			neu_aver = np.mean(neu)
			if neu_aver < neg_aver: result = 0
	return result

for i in range(1, page):
	url = 'https://section.blog.naver.com/Search/Post.naver?pageNo=' + str(i) + '&rangeType=MONTH&orderBy=sim&startDate=' + before_one_month + '&endDate=' + now + '&keyword=' + text
	driver.get(url)
	time.sleep(1)

	for j in range(1, 8):
		titles = driver.find_element(By.XPATH, '/html/body/ui-view/div/main/div/div/section/div[2]/div['+str(j)+']/div/div[1]/div[1]/a[1]')
		title = titles.get_attribute('href')
		url_list.append(title)

print("url 수집 끝, 해당 url 데이터 크롤링")

for url in url_list: # 수집한 url 만큼 반복
	driver.get(url) # 해당 url로 이동
 
	driver.switch_to.frame('mainFrame')
	overlays = ".se-text"
	contents = driver.find_elements(By.CSS_SELECTOR, overlays)

	for content in contents:
		content_list = content_list + content.text # content_list 라는 값에 + 하면서 점점 누적 (블로그 내용 text)

	wine = get_count(content_list)
	score = []  # 리뷰 하나 당 감정 분석을 위한 점수 배열
	if wine:
		nouns = okt.nouns(content_list)
		sentence = sent_tokenize(content_list)
		access = list(set(filter(get_access, nouns)))
		taste_sen =  list(filter(get_taste, sentence))
		for text in taste_sen:
			score.append(sia.polarity_scores(text))
		emotion = get_average(score)
		present = list(set(filter(get_present, nouns)))
		result.append([url, emotion, wine, access, present])
	content_list = ''

df = pd.DataFrame(result, columns=["url", "emotion" ,"wine", "access", "present"]) # 결과를 데이터 프레임으로 저장

address = 'C:/Users/limga/OneDrive/Desktop/data/blogCrawling/'
df.to_csv(path_or_buf=address+'blog_crawling.csv', encoding="utf-8-sig", index=False)