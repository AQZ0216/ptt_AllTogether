import numpy as np
import pandas as pd
import json
import jieba
from wordcloud import WordCloud
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.family'] = ['Noto Sans CJK TC'] # Windwos
# mpl.rcParams['font.family'] = ['Noto Sans CJK JP'] # Ubuntu

with open('text.json') as f:
    text = json.load(f)

f = open("stopWords.txt", "r", encoding='UTF-8')
string = f.read()
stopWords = list(string.split("\n"))
#%%
length = len(text)

i = np.arange(length)

zipped = list(zip(i, text))

df = pd.DataFrame(zipped , columns=['i', 'text'])

#%% Jeiba
jieba.set_dictionary('dict.txt.big.txt')
jieba.load_userdict('dict.txt')

record = {}

words_list = []


for i in range(length):
    seg_list = jieba.cut(df['text'][i])
    remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', seg_list))
    words_list.append(remainderWords)
    
    for key in remainderWords:
        value = record.get(key, 0)
        record[key] = value+1
        
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

def loc(loc_dict, loc_list):
    loc_dict['基隆'] += loc_list[1]
    loc_dict['台北'] += any(loc_list[2:3])
    loc_dict['新北'] += loc_list[4]
    loc_dict['桃園'] += loc_list[6]
    loc_dict['新竹'] += loc_list[7]
    loc_dict['宜蘭'] += loc_list[8]
    loc_dict['苗栗'] += loc_list[10]
    loc_dict['台中'] += any(loc_list[11:12])
    loc_dict['南投'] += loc_list[14]
    loc_dict['雲林'] += loc_list[15]
    loc_dict['嘉義'] += loc_list[17]
    loc_dict['台南'] += any(loc_list[18:19])
    loc_dict['高雄'] += loc_list[20]
    loc_dict['屏東'] += loc_list[21]
    loc_dict['花蓮'] += loc_list[23]
    loc_dict['台東'] += any(loc_list[24:25])
    loc_dict['澎湖'] += loc_list[28]
    loc_dict['金門'] += loc_list[29]
    loc_dict['馬祖'] += loc_list[30]

def region(region_dict, loc_list):
    region_dict['北部'] += any(loc_list[0:9])
    region_dict['中部'] += any(loc_list[10:15])
    region_dict['南部'] += any(loc_list[16:21])
    region_dict['東部+離島'] += any(loc_list[22:30])

signs = ['牡羊', '金牛', '雙子', '巨蟹', '獅子', '處女', '天秤', '天蠍', '射手', '摩羯', '水瓶', '雙魚', '蠍子']
location = ['北部', '基隆', '台北', '臺北', '新北', '雙北', '桃園', '新竹', 
            '宜蘭', '中部', '苗栗', '台中', '臺中', '彰化', '南投', '雲林', 
            '南部', '嘉義', '台南', '臺南', '高雄', '屏東', '東部', '花蓮', 
            '台東', '臺東', '花東', '離島', '澎湖', '金門', '馬祖']


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
df['my_signs'] = ''
df['your_signs'] = ''
df['my_loc'] = ''
df['your_loc'] = ''

df['cig'] = ''
df['alc'] = ''

about_me_words_idx_list = []
about_you_words_idx_list = []
about_me_str_idx_list = []
about_you_str_idx_list = []

my_signs_dict = dict.fromkeys(signs[0:12], 0)
your_signs_dict = dict.fromkeys(signs[0:12], 0)
my_loc_dict = {'基隆':0, '台北':0, '新北':0, '桃園':0, '新竹':0, '宜蘭': 0, 
            '苗栗':0, '台中':0, '彰化':0, '南投':0, '雲林':0, '嘉義':0, 
            '台南':0, '高雄':0, '屏東':0, '花蓮':0, '台東':0, '澎湖':0, 
            '金門':0, '馬祖':0}
your_loc_dict = {'基隆':0, '台北':0, '新北':0, '桃園':0, '新竹':0, '宜蘭': 0, 
            '苗栗':0, '台中':0, '彰化':0, '南投':0, '雲林':0, '嘉義':0, 
            '台南':0, '高雄':0, '屏東':0, '花蓮':0, '台東':0, '澎湖':0, 
            '金門':0, '馬祖':0}
my_region_dict = {'北部': 0, '中部':0, '南部' : 0, '東部+離島' : 0}
your_region_dict = {'北部': 0, '中部':0, '南部' : 0, '東部+離島' : 0}

my_loc_sum = 0
your_loc_sum = 0


for i in range(length):
    about_me_words_idx = [None,None]
    about_you_words_idx = [None,None]
    about_me_str_idx = [None,None]
    about_you_str_idx = [None,None]
    
    ## about me & about you
    about_me_words_idx[0] = about_me(words_list[i], 0)
    if about_me_words_idx[0] != None:
        about_me_words_idx[1] = about_you(words_list[i], about_me_words_idx[0])
    else:
        about_me_words_idx = [-1, -1]
    about_me_words_idx_list.append(about_me_words_idx)
        
    about_you_words_idx[0] = about_you(words_list[i], 0)
    if about_you_words_idx[0] != None:
        about_you_words_idx[1] = about_me(words_list[i], about_you_words_idx[0])
    else:
        about_you_words_idx = [-1, -1]
    about_you_words_idx_list.append(about_you_words_idx)
    
    about_me_str_idx[0] = df['text'][i].find('關於我')
    if about_me_str_idx[0] != -1:
        about_me_str_idx[1] = df['text'][i].find('關於你', about_me_str_idx[0])
        if about_me_str_idx[1] == -1:
            about_me_str_idx[1] = df['text'][i].find('希望你', about_me_str_idx[0])
        if about_me_str_idx[1] == -1:   
            about_me_str_idx[1] = None
    else:
        about_me_str_idx = [-1, -1]
    about_me_str_idx_list.append(about_me_str_idx)
            
    about_you_str_idx[0] = df['text'][i].find('關於你')
    if about_you_str_idx[0] == -1:
        about_you_str_idx[0] = df['text'][i].find('希望你')
    if about_you_str_idx[0] != -1:
        about_you_str_idx[1] = df['text'][i].find('關於我', about_you_str_idx[0])
        if about_you_str_idx[1] == -1:
            about_you_str_idx[1] = None
    else:
        about_you_str_idx = [-1, -1]
    about_you_str_idx_list.append(about_you_str_idx)
    
    
    ## deal w/ 年次
    num_idx = -1
    try:
        num_idx = words_list[i].index('年次', about_me_words_idx[0], about_me_words_idx[1])
    except TypeError:
        try:
            num_idx = words_list[i].index('年次', about_me_words_idx[0])
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
        num_idx = words_list[i].index('年次', about_you_words_idx[0], about_you_words_idx[1])
    except TypeError:
        try:
            num_idx = words_list[i].index('年次', about_you_words_idx[0])
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
    for j in words_list[i][about_me_words_idx[0]: about_me_words_idx[1]]:
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
    
    for j in words_list[i][about_you_words_idx[0]: about_you_words_idx[1]]:
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
    
    
    ## signs&loc
    my_signs_dict_temp = dict.fromkeys(signs, False)
    your_signs_dict_temp = dict.fromkeys(signs, False)
    for j in signs:
        my_signs_dict_temp[j] = (j in df['text'][i][about_me_str_idx[0]: about_me_str_idx[1]])
        your_signs_dict_temp[j] = (j in df['text'][i][about_you_str_idx[0]: about_you_str_idx[1]])
        if j in df['text'][i][about_me_str_idx[0]: about_me_str_idx[1]]:
            df['my_signs'][i] += j
        if j in df['text'][i][about_you_str_idx[0]: about_you_str_idx[1]]:
            df['your_signs'][i] += j

    my_loc_list = []
    your_loc_list = []
    for j in location:
        my_loc_list.append(j in df['text'][i][about_me_str_idx[0]: about_me_str_idx[1]])
        your_loc_list.append(j in df['text'][i][about_you_str_idx[0]: about_you_str_idx[1]])
        if j in df['text'][i][about_me_str_idx[0]: about_me_str_idx[1]]:
            df['my_loc'][i] += j
        if j in df['text'][i][about_you_str_idx[0]: about_you_str_idx[1]]:
            df['your_loc'][i] += j

    for j in signs:
        if j != '天蠍' and j != '蠍子':
            my_signs_dict[j] += my_signs_dict_temp[j]
    my_signs_dict['天蠍'] += my_signs_dict_temp['天蠍'] or my_signs_dict_temp['蠍子']
    for j in signs:
        if j != '天蠍' and j != '蠍子':
            your_signs_dict[j] += your_signs_dict_temp[j]
    your_signs_dict['天蠍'] += your_signs_dict_temp['天蠍'] or your_signs_dict_temp['蠍子']
    
    loc(my_loc_dict, my_loc_list)
    loc(your_loc_dict, your_loc_list)
    region(my_region_dict, my_loc_list)
    region(your_region_dict, your_loc_list)
    my_loc_sum += any(my_loc_list[1:4]+my_loc_list[6:8]+my_loc_list[10:15]+
                      my_loc_list[17:21]+my_loc_list[23:25]+my_loc_list[28:30])
    your_loc_sum += any(your_loc_list[1:4]+your_loc_list[6:8]+your_loc_list[10:15]+
                       your_loc_list[17:21]+your_loc_list[23:25]+your_loc_list[28:30])
    
    
    # cat&dog
    df['cat'][i] = '貓' in df['text'][i]
    df['dog'][i] = '狗' in df['text'][i]
    df['me_cat'][i] = '貓' in df['text'][i][about_me_str_idx[0]: about_me_str_idx[1]]
    df['me_dog'][i] = '狗' in df['text'][i][about_me_str_idx[0]: about_me_str_idx[1]]
    df['you_cat'][i] = '貓' in df['text'][i][about_you_str_idx[0]: about_you_str_idx[1]]
    df['you_dog'][i] = '狗' in df['text'][i][about_you_str_idx[0]: about_you_str_idx[1]]
    
    df['cig'][i] = '菸' in df['text'][i]
    df['alc'][i] = '酒' in df['text'][i]

#%% plot word freq
record_sort = sorted(record.items(), key=lambda x:x[1], reverse=True)
rank = list(zip(*record_sort))

plt.figure(figsize=[9.6, 4.8])
x = np.arange(20)
plt.bar(x, rank[1][0:20])
plt.xticks(x, rank[0][0:20])
plt.savefig('word_freq.png', dpi=200)
plt.show()

#%% wordcloud
font_path = "NotoSansCJKtc-Regular.otf"
couple_mask = np.array(Image.open("couple.png"))

wordcloud = WordCloud(background_color="white", mask=couple_mask, font_path=font_path).generate_from_frequencies(record)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
wordcloud.to_file("wordcloud.png")

#%%
me_record = {}
you_record = {}

for i in range(length):
    for key in words_list[i][about_me_words_idx_list[i][0] : about_me_words_idx_list[i][1]]:
        value = me_record.get(key, 0)
        me_record[key] = value+1
        
for i in range(length):
    for key in words_list[i][about_you_words_idx_list[i][0] : about_you_words_idx_list[i][1]]:
        value = you_record.get(key, 0)
        you_record[key] = value+1

#%%
record_sort = sorted(me_record.items(), key=lambda x:x[1], reverse=True)
rank = list(zip(*record_sort))

plt.figure(figsize=[9.6, 4.8])
x = np.arange(20)
plt.bar(x, rank[1][0:20])
plt.xticks(x, rank[0][0:20])
plt.savefig('me_word_freq.png', dpi=200)
plt.show()

record_sort = sorted(you_record.items(), key=lambda x:x[1], reverse=True)
rank = list(zip(*record_sort))

plt.figure(figsize=[9.6, 4.8])
x = np.arange(20)
plt.bar(x, rank[1][0:20])
plt.xticks(x, rank[0][0:20])
plt.savefig('you_word_freq.png', dpi=200)
plt.show()

#%% wordcloud
heart_mask = np.array(Image.open("heart.jpg"))

wordcloud = WordCloud(background_color="white", mask=heart_mask, font_path=font_path).generate_from_frequencies(me_record)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
wordcloud.to_file("me_wordcloud.png")

wordcloud = WordCloud(background_color="white", mask=heart_mask, font_path=font_path).generate_from_frequencies(you_record)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
wordcloud.to_file("you_wordcloud.png")

#%% plot figures
plt.hist(df['my_age'], bins=7, range=(15, 50))
plt.title("關於我：年齡, N = " + str(sum(df['my_age'] != 0)))
plt.savefig('my_age.png', dpi=200)
plt.show()
plt.hist(df['my_height'], bins=11, range=(140, 195))
plt.title("關於我：身高, N = " + str(sum(df['my_height'] != 0)))
plt.savefig('my_height.png', dpi=200)
plt.show()
plt.hist(df['my_weight'], bins=12, range=(40, 100))
plt.title("關於我：體重, N = " + str(sum(df['my_weight'] != 0)))
plt.savefig('my_weight.png', dpi=200)
plt.show()
plt.hist(df['your_age'], bins=7, range=(15, 50))
plt.title("關於你：年齡, N = " + str(sum(df['your_age'] != 0)))
plt.savefig('your_age.png', dpi=200)
plt.show()
plt.hist(df['your_height'], bins=11, range=(140, 195))
plt.title("關於你：身高, N = " + str(sum(df['your_height'] != 0)))
plt.savefig('your_height.png', dpi=200)
plt.show()
plt.hist(df['your_weight'], bins=12, range=(40, 100))
plt.title("關於你：體重, N = " + str(sum(df['your_weight'] != 0)))
plt.savefig('your_weight.png', dpi=200)
plt.show()

#%% plot loc&region
plt.bar(my_signs_dict.keys(), my_signs_dict.values())
plt.title("關於我：星座, N = " +  str(sum(df['my_signs'] != '')))
plt.savefig('my_signs.png', dpi=200)
plt.show()

plt.bar(your_signs_dict.keys(), your_signs_dict.values())
plt.title("關於你：星座, N = " +  str(sum(df['your_signs'] != '')))
plt.savefig('your_signs.png', dpi=200)
plt.show()

plt.figure(figsize=[8, 4.8])
plt.bar(my_loc_dict.keys(), my_loc_dict.values())
plt.title("關於我：縣市, N = " + str(my_loc_sum))
plt.savefig('my_loc.png', dpi=200)
plt.show()

plt.figure(figsize=[8, 4.8])
plt.bar(your_loc_dict.keys(), your_loc_dict.values())
plt.title("關於你：縣市, N = " + str(your_loc_sum))
plt.savefig('your_loc.png', dpi=200)
plt.show()

plt.pie(my_region_dict.values(), labels=my_region_dict.keys() ,autopct='%1.1f%%')
plt.axis('equal')
plt.title("關於我：區域, N = " + str(sum(df['my_loc'] != '')))
plt.savefig('my_region.png', dpi=200)
plt.show()

plt.pie(your_region_dict.values(), labels=your_region_dict.keys() ,autopct='%1.1f%%')
plt.axis('equal')
plt.title("關於你：區域, N = " + str(sum(df['your_loc'] != '')))
plt.savefig('your_region.png', dpi=200)
plt.show()

#%% plot cat&dog
x = ['cat', 'dog']
cat = sum(df['cat'])
dog = sum(df['dog'])
me_cat = sum(df['me_cat'])
me_dog = sum(df['me_dog'])
you_cat = sum(df['you_cat'])
you_dog = sum(df['you_dog'])

plt.bar(x, [cat, dog])
plt.title("貓狗, N = " + str(cat+dog))
plt.savefig('cat_dog.png', dpi=200)
plt.show()
plt.bar(x, [me_cat, me_dog])
plt.title("關於我：貓狗, N = " + str(me_cat+me_dog))
plt.savefig('me_cat_dog.png', dpi=200)
plt.show()
plt.bar(x, [you_cat, you_dog])
plt.title("關於你：貓狗, N = " + str(you_cat+you_dog))
plt.savefig('you_cat_dog.png', dpi=200)
plt.show()