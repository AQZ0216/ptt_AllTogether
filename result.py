import json
import pandas as pd
import re
import jieba

with open('text.json') as f:
    text = json.load(f)

#%%
df = pd.DataFrame(text, columns=['text'])

#%%
f = open("stopWords.txt", "r", encoding='UTF-8')
string = f.read()
stopWords = list(string.split("\n")) 

#%% Jeiba
seg_list = []
jieba.set_dictionary('dict.txt.big.txt')

seg_list = jieba.cut(df['text'][0])
# temp = " ".join(seg_list)
remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', seg_list))

#%%
length = len(df)

df['me'] = 0
df['you'] = 0
df['yr'] = 0
df['age'] = 0
df['height'] = 0
df['weight'] = 0
df['intro'] = 0
# temp1 = []

for i in range(length):
    df['me'][i] = df['text'][i].find('關於我')
    df['you'][i] = df['text'][i].find('關於你')
    df['intro'][i] = df['text'][i].find('自我介紹')
    if df['you'][i] == -1:
        df['you'][i] = df['text'][i].find('希望你')
    
    temp = re.findall(r'\d+', df['text'][i]) 
    res = list(map(int, temp)) 
    # temp1.append(res)
    
    for j in res:
        if 2002 >= j > 1970 and df['yr'][i] == 0:
            df['yr'][i] = j
        if 40 >= j >= 18 and df['age'][i] == 0:
            df['age'][i] = j
        if 195 > j > 140 and df['height'][i] == 0:
            df['height'][i] = j
        if 100 > j > 40 and df['weight'][i] == 0:
            df['weight'][i] = j