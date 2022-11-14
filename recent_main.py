import pandas as pd
import numpy as np
import itertools
import json

wine_list = pd.read_csv('wine_list.csv', encoding='utf-8')
wine_check = pd.read_csv('recent_crawling.csv', encoding='utf-8')
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
		wine_name.append(eval(wine_check._get_value(i, 'wine')))
	wine = list(itertools.chain.from_iterable(wine_name))
	return wine

# 와인 이름 배열
wine_name = set(get_name())

# 언급된 와인 정보 얻는 함수
def get_info():
	wine_info = []
	for wine in wine_name:
		val = wine_list_df.loc[wine_list['wineName'] == wine].values.tolist()
		wine_info.append(val)
	return wine_info

wine_info_arr = np.array(flatten(get_info()), dtype=object)
wine_info_df = pd.DataFrame(wine_info_arr)
wine_info_df.columns=["wineImage", "wineName", "wineNameEng", "wineType", "winePrice", "wineSweet", "wineBody", "wineVariety", "aroma1", "aroma2", "aroma3"]

data_json = wine_info_df.to_json(orient = 'records')
parsed = json.loads(data_json)

with open('./recent_data.json', 'w', encoding='utf-8') as f:
	json.dump(parsed, f, indent=4, ensure_ascii=False)
