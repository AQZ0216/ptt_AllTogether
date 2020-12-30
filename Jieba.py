import numpy as np
import pandas as pd
import json
import jieba
import matplotlib as mpl
import matplotlib.pyplot as plt

import re

mpl.rcParams['font.family'] = ['Noto Sans CJK TC']

with open('text.json') as f:
    text = json.load(f)

f = open("stopWords.txt", "r", encoding='UTF-8')
string = f.read()
stopWords = list(string.split("\n"))
#%%
df = pd.DataFrame(text, columns=['text'])

#%% Jeiba
jieba.set_dictionary('dict.txt.big.txt')
jieba.load_userdict('dict.txt')

record = {}

word = []

length = len(df)
for i in range(length):
    seg_list = jieba.cut(df['text'][i])
    remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', seg_list))
    
    word.append(remainderWords)
    
    for key in remainderWords:
        value = record.get(key, 0)
        record[key] = value+1
        
record_sort = sorted(record.items(), key=lambda x:x[1], reverse=True)
rank = list(zip(*record_sort))

x = np.arange(10)
plt.bar(x, rank[1][0:10])
plt.xticks(x, rank[0][0:10])

#%%
df['me'] = 0
df['you'] = 0
# df['yr'] = 0
df['age'] = 0
df['height'] = 0
df['weight'] = 0
df['loc'] = 0

for i in range(length):
    df['me'][i] = df['text'][i].find('關於我')
    df['you'][i] = df['text'][i].find('關於你')
    if df['you'][i] == -1:
        df['you'][i] = df['text'][i].find('希望你')
    
    temp = re.findall(r'\d+', df['text'][i])
    res = list(map(int, temp)) 
    # temp1.append(res)
    
    for j in res:
        if 2002 >= j > 1970 and df['age'][i] == 0:
            df['age'][i] = 2020-j
        if 40 >= j >= 18 and df['age'][i] == 0:
            df['age'][i] = j
        if 195 > j > 140 and df['height'][i] == 0:
            df['height'][i] = j
        if 100 > j > 40 and df['weight'][i] == 0:
            df['weight'][i] = j

#%%

location = ['台北', '新北', '雙北', '桃園', '新竹', '苗栗', '台中', '彰化', '南投', '雲林', '嘉義', '台南', '高雄', '屏東', '宜蘭', '花蓮', '台東', '澎湖', '金門', '馬祖', '北部', '中部', '南部', '東部', '離島']
for i in range(length):
    for j in word[i]:
        for k in location:
            if j == k:
                df['loc'][i] = j
    

#%%
plt.hist(df['age'], bins=[15, 20, 25, 30, 35, 40, 45, 50])
plt.show()
plt.hist(df['height'], bins=11, range=(140, 195))
plt.show()
plt.hist(df['weight'], bins=12, range=(40, 100))
plt.show()
plt.bar(df['weight'], rank[1][0:10])
plt.show()
