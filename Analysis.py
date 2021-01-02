import numpy as np
import pandas as pd
import json
import jieba
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.family'] = ['Noto Sans CJK JP']

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

words_list = []

length = len(df)
for i in range(length):
    seg_list = jieba.cut(df['text'][i])
    remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', seg_list))
    words_list.append(remainderWords)
    
    for key in remainderWords:
        value = record.get(key, 0)
        record[key] = value+1
        
#%% plot word freq
record_sort = sorted(record.items(), key=lambda x:x[1], reverse=True)
rank = list(zip(*record_sort))

x = np.arange(10)
plt.bar(x, rank[1][0:10])
plt.xticks(x, rank[0][0:10])
plt.savefig('word_freq.png')

#%%
def about_me(words_list, start):
    try:
        return words_list.index('關於我', start)
    except ValueError:
        return None

def about_you(words_list, start):
    try:
        return words_list.index('關於你', start)
    except ValueError:
        try:
            return words_list.index('希望你', start)
        except ValueError:
            return None


signs = ['牡羊', '金牛', '雙子', '巨蟹', '獅子', '處女', '天秤', '天蠍', '射手', '摩羯', '水瓶', '雙魚', '蠍子']
location = ['北部', '基隆', '台北', '臺北', '新北', '雙北', '桃園', '新竹', 
            '宜蘭', '中部', '苗栗', '台中', '臺中', '彰化', '南投', '雲林', 
            '南部', '嘉義', '台南', '臺南', '高雄', '屏東', '東部', '花蓮', 
            '台東', '臺東', '花東', '離島', '澎湖', '金門', '馬祖']

region_dict = {'北部': 0, '中部':0, '南部' : 0, '東部' : 0, '離島' : 0}


about_me_list = []
about_you_list = []

df['my_age'] = 0
df['my_height'] = 0
df['my_weight'] = 0
df['your_age'] = 0
df['your_height'] = 0
df['your_weight'] = 0
df['cat'] = False
df['dog'] = False
df['me_cat'] = False
df['me_dog'] = False
df['you_cat'] = False
df['you_dog'] = False

signs_list = []
loc_list = []

me_cat = 0
you_cat = 0
me_dog = 0
you_dog = 0

for i in range(length):
    ## about me & about you
    about_me_begin = about_me(words_list[i], 0)
    if about_me_begin != None:
        about_me_end = about_you(words_list[i], about_me_begin)
    else:
        about_me_begin = -1
        about_me_end = -1
    about_me_list.append((about_me_begin , about_me_end))
        
    about_you_begin = about_you(words_list[i], 0)
    if about_you_begin != None:
        about_you_end = about_me(words_list[i], about_you_begin)
    else:
        about_you_begin = -1
        about_you_end = -1
    about_you_list.append((about_you_begin , about_you_end))
    
    ## deal w/ 年次
    num_idx = -1
    try:
        num_idx = words_list[i].index('年次', about_me_begin, about_me_end)
    except TypeError:
        try:
            num_idx = words_list[i].index('年次', about_me_begin)
        except ValueError:
            pass
    except ValueError:
        pass
        
    if num_idx != -1:
        try:
            num = int(words_list[i][num_idx-1])
        except:
            num = -1
        
        if 91 >= num >= 65 and df['my_age'][i] == 0:
            df['my_age'][i] = 109-num
            words_list[i][num_idx-1] = ''
            
        try:
            num = int(words_list[i][num_idx+1])
        except:
            num = -1
            
        if 91 >= num >= 65 and df['my_age'][i] == 0:
            df['my_age'][i] = 109-num
            words_list[i][num_idx+1] = ''
        
    num_idx = -1
    try:
        num_idx = words_list[i].index('年次', about_you_begin, about_you_end)
    except TypeError:
        try:
            num_idx = words_list[i].index('年次', about_you_begin)
        except ValueError:
            pass
    except ValueError:
        pass
    
    if num_idx != -1:
        try:
            num = int(words_list[i][num_idx-1])
        except:
            num = -1
        
        if 91 >= num >= 65 and df['your_age'][i] == 0:
            df['your_age'][i] = 109-num
            words_list[i][num_idx-1] = ''
            
        try:
            num = int(words_list[i][num_idx+1])
        except:
            num = -1
            
        if 91 >= num >= 65 and df['your_age'][i] == 0:
            df['your_age'][i] = 109-num
            words_list[i][num_idx+1] = ''
            
    ## deal w/ numbers
    for j in words_list[i][about_me_begin: about_me_end]:
        try:
            num = float(j)
            if 2002 >= num > 1970 and df['my_age'][i] == 0:
                df['my_age'][i] = 2020-num
            if 40 >= num >= 18 and df['my_age'][i] == 0:
                df['my_age'][i] = num
            if 195 > num > 140 and df['my_height'][i] == 0:
                df['my_height'][i] = num
            if 100 > num > 40 and df['my_weight'][i] == 0:
                df['my_weight'][i] = num
        except:
            pass
    
    for j in words_list[i][about_you_begin: about_you_end]:
        try:
            num = float(j)
            if 2002 >= num > 1970 and df['your_age'][i] == 0:
                df['your_age'][i] = 2020-num
            if 40 >= num >= 18 and df['your_age'][i] == 0:
                df['your_age'][i] = num
            if 195 > num > 140 and df['your_height'][i] == 0:
                df['your_height'][i] = num
            if 100 > num > 40 and df['your_weight'][i] == 0:
                df['your_weight'][i] = num
        except:
            pass
    
    
    signs_list.append([])
    for j in signs:
        if j in words_list[i][about_me_begin: about_me_end]:
             signs_list[i].append(j)
        if j in words_list[i][about_you_begin: about_you_end]:
             print(i, j)
    
    # cat&dog
    df['cat'][i] = '貓' in words_list[i]
    df['dog'][i] = '狗' in words_list[i]
    df['me_cat'][i] = '貓' in words_list[i][about_me_begin: about_me_end]
    df['me_dog'][i] = '狗' in words_list[i][about_me_begin: about_me_end]
    df['you_cat'][i] = '貓' in words_list[i][about_you_begin: about_you_end]
    df['you_dog'][i] = '狗' in words_list[i][about_you_begin: about_you_end]


#    loc_list.append([])
#    for j in location:
#        if j in words_list[i][about_me_begin: about_me_end]:
#             signs_list[i].append(j)
#        if j in words_list[i][about_you_begin: about_you_end]:
#             print(i, j)
        
#%%
signs = ['牡羊', '金牛', '雙子', '巨蟹', '獅子', '處女', '天秤', '天蠍', '射手', '摩羯', '水瓶', '雙魚']
freq2 = [0]*len(signs)
for i in range(len(signs)):
    for j in range(length):
        signs_list.append([])
        for k in word[j]:
            if signs[i] in k:
                signs_list[j].append(k)
                freq2[i] += 1
                break


#%%
loc_list = []
region_list = []
#loc_dict = {'基隆':0, '台北':0, '臺北':0, '新北':0, '桃園':0, '新竹':0, '宜蘭': 0, 
#'苗栗', 
#'台中', 
#'臺中', 
#'彰化', 
#'南投', 
#'雲林', 
#'南部', 
#'嘉義', 
#'台南', 
#'臺南', 
#'高雄', 
#'屏東', 
#'東部', 
#'花蓮', 
#'台東', 
#'臺東', 
#'離島', 
#'澎湖', 
#'金門', 
#'馬祖'}


freq = [0]*len(location)
for i in range(len(location)):
    for j in range(length):
        loc_list.append([])
        for k in word[j]:
            if location[i] in k:
                loc_list[j].append(k)
                freq[i] += 1
                break

#%%
plt.hist(df['my_age'], bins=7, range=(15, 50))
plt.title("關於我：年齡, N = " + str(sum(df['my_age'] != 0)))
plt.savefig('my_age.png')
plt.show()
plt.hist(df['my_height'], bins=11, range=(140, 195))
plt.title("關於我：身高, N = " + str(sum(df['my_height'] != 0)))
plt.savefig('my_height.png')
plt.show()
plt.hist(df['my_weight'], bins=12, range=(40, 100))
plt.title("關於我：體重, N = " + str(sum(df['my_weight'] != 0)))
plt.savefig('my_weight.png')
plt.show()
plt.hist(df['your_age'], bins=7, range=(15, 50))
plt.title("關於你：年齡, N = " + str(sum(df['your_age'] != 0)))
plt.savefig('your_age.png')
plt.show()
plt.hist(df['your_height'], bins=11, range=(140, 195))
plt.title("關於你：身高, N = " + str(sum(df['your_height'] != 0)))
plt.savefig('your_height.png')
plt.show()
plt.hist(df['your_weight'], bins=12, range=(40, 100))
plt.title("關於你：體重, N = " + str(sum(df['your_weight'] != 0)))
plt.savefig('your_weight.png')
plt.show()


x = ['cat', 'dog']

cat = sum(df['cat'])
dog = sum(df['dog'])
me_cat = sum(df['me_cat'])
me_dog = sum(df['me_dog'])
you_cat = sum(df['you_cat'])
you_dog = sum(df['you_dog'])

plt.bar(x, [cat, dog])
plt.title("貓狗, N = " + str(cat+dog))
plt.savefig('cat_dog.png')
plt.show()
plt.bar(x, [me_cat, me_dog])
plt.title("關於我：貓狗, N = " + str(me_cat+me_dog))
plt.savefig('me_cat_dog.png')
plt.show()
plt.bar(x, [you_cat, you_dog])
plt.title("關於你：貓狗, N = " + str(you_cat+you_dog))
plt.savefig('you_cat_dog.png')
plt.show()

#plt.bar(location, freq)
#plt.show()
#plt.bar(signs, freq2)
#plt.show()