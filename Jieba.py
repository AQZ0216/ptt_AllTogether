import numpy as np
import pandas as pd
import json
import jieba
import matplotlib as mpl
import matplotlib.pyplot as plt


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

record = {}

length = len(df)
for i in range(length):
    seg_list = jieba.cut(df['text'][i])
    remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', seg_list))
    for key in remainderWords:
        value = record.get(key, 0)
        record[key] = value+1
        
record_sort = sorted(record.items(), key=lambda x:x[1], reverse=True)
rank = list(zip(*record_sort))

x = np.arange(10)
plt.bar(x, rank[1][0:10])
plt.xticks(x, rank[0][0:10])