from collections import Counter

import pandas as pd
import numpy as np
import random
import itertools

wine_result = pd.read_csv('wine_result.csv', encoding='utf-8')
crawling_result = pd.read_csv('blog_crawling.csv', encoding='utf-8')

def flatten(arg):
	ret = []
	for i in arg:
		ret.extend(i) if isinstance(i, list) else ret.append(i)
	return ret

def extraction(arr):
	wine_cnt = len(arr)
	result = Counter(arr).most_common()
  
	if (wine_cnt > 4):
		if (len(set(np.array(result).T[1])) > 1):
			return np.array(result[0:5]).T[0]
		else:
			return random.sample(list(np.array(result[0:5]).T[0]), 5)
	else:
		if (len(set(np.array(result).T[1])) > 1):
			return np.array(result).T[0]
		else:
			return random.sample(list(np.array(result).T[0]), wine_cnt)

# 와인 언급 횟수 top 5
def mention():
	wine_cnt = len(wine_result)
	if (wine_cnt > 4):
		wine_mention = np.array(wine_result.values[0:5]).T[1]
		wine_mention_count = np.array(wine_result.values[0:5]).T[4]  
	else:
		wine_mention = np.array(wine_result.values).T[1]
		wine_mention_count = np.array(wine_result.values).T[4] 

	if(len(set(wine_mention_count)) <= 1):
		return random.sample(list(wine_mention), len(wine_mention))
	else:
		return wine_mention

# 접근성 top 5
def access():
	wine_access = []
	for i in crawling_result.index:
		access = eval(crawling_result._get_value(i, 'access'))
		if (len(access) > 0):
			wine_access.append(eval(crawling_result._get_value(i, 'wine')))
	wine = list(itertools.chain.from_iterable(wine_access))
	return extraction(wine)

# 선물 top 5
def present():
	wine_present = []
	for i in crawling_result.index:
		present = eval(crawling_result._get_value(i, 'present'))
		if (len(present) > 0):
			wine_present.append(eval(crawling_result._get_value(i, 'wine')))
	wine = list(itertools.chain.from_iterable(wine_present))
	return extraction(wine)

# 가성비 top 5
def cost():
	df = wine_result[['이름', '가격']]
	wine_cost_list = sorted(df.values.tolist(), key=lambda x:x[1])
	wine_cnt = len(wine_cost_list)

	if (wine_cnt > 4):
		wine_cost_list = wine_cost_list[0:5]
  
  	# 와인 가격만 추출 (동일하면 랜덤으로 와인 뽑기 위해)
	wine_cost = [i[1] for i in wine_cost_list]
	wine_name = np.array(wine_cost_list).T[0]
	if (len(set(wine_cost)) > 1):
		return wine_name
	else:
		return random.sample(list(wine_name), len(wine_name))

print(mention())
print(access())
print(present())
print(cost())




