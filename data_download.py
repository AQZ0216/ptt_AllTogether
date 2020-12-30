import requests
from bs4 import BeautifulSoup
import bs4.element
import json

text_list = []

n = 222

for i in range(1, n):
    r1 = requests.get('https://www.ptt.cc/bbs/AllTogether/search?page=' + str(i) + '&q=%5B%E5%BE%B5%E7%94%B7%5D')
    soup1 = BeautifulSoup(r1.text, 'html.parser')

    href = []

    a_tags = soup1.find_all('a')
    for tag in a_tags:
        if('[徵男]' in tag.get_text()):
            href.append(tag.get('href'))
    
    for ref in href:
        r2 = requests.get('https://www.ptt.cc' + ref)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        
        content = soup2.find(id="main-content")
        
        if content != None:
            a_tags = content.find_all('a')
            for tag in a_tags:
                tag.extract()
            pic_tags = content.find_all(class_='richcontent')
            for tag in pic_tags:
                tag.extract()
            f2_tags = content.find_all(class_='f2')
            for tag in f2_tags:
                tag.extract()     
            f6_tags = content.find_all(class_='f6')
            for tag in f6_tags:
                tag.extract() 
            
            meta_tags = content.find_all(class_='article-metaline')
            if(len(meta_tags) != 0):
                p = meta_tags[-1].next_sibling
                
                text = ''
                while(type(p) == bs4.element.NavigableString):
                    text += str(p)
                    p = p.next_sibling
                
                text_list.append(text)
    print(i)
                
#%%
with open('text.json', 'w') as f:
    json.dump(text_list, f)