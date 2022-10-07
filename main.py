from collections import Counter
import pandas as pd
import numpy as np

wine_list = pd.read_csv('wine_list.csv', encoding='utf-8')
wine_check = pd.read_csv('blog_crawling.csv', encoding='utf-8')
wine_list_df =  pd.DataFrame(wine_list)

def flatten(arg):
	ret = []
	for i in arg:
		ret.extend(i) if isinstance(i, list) else ret.append(i)
	return ret

# 언급된 와인 이름 얻는 함수
def get_name():
	wine_name = []
	for i in wine_check.index:
		name_str = wine_check._get_value(i, 'wine').replace("[","").replace("]","").replace("'","")
		wine_name.append(name_str.split(','))
	return wine_name

# 와인 이름, 언급 횟수 튜플
wine_mention = Counter(flatten(get_name())).most_common()
# 와인 이름 배열
wine_name = []
# 와인 언급 횟수 배열
wine_count = []

for wine in wine_mention:
	wine_name.append(wine[0])
	wine_count.append(wine[1])

# 언급된 와인 정보 얻는 함수
def get_info():
	wine_info = []
	for wine in wine_name:
		val = wine_list_df.loc[wine_list['이름'] == wine].values.tolist()
		wine_info.append(val)
	return wine_info

wine_info_arr = np.array(flatten(get_info()), dtype=object)
wine_info_df = pd.DataFrame(wine_info_arr)
wine_info_df.columns=["이미지", "이름", "영문이름", "종류", "가격", "당도", "바디", "아로마1", "아로마2", "아로마3", "품종"]

wine_info_df.insert(4, '언급 횟수', wine_count)

address = 'C:/Users/limga/OneDrive/Desktop/data/blogCrawling/'
wine_info_df.to_csv(path_or_buf=address+'wine_result.csv', encoding="utf-8-sig", index=False)
