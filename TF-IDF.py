# -*- coding: utf-8 -*-
"""
Created on Sat Jul 02 15:53:32 2016

@author: Administrator
"""

import jieba
import pandas as pd
import numpy as np
from collections import Counter
from collections import defaultdict

from wordcloud import WordCloud
from os import path
import matplotlib.pyplot as plt


dir_path="C:\\Users\\Administrator\\Desktop\\Sample\\C000007\\"
stopwords = {}.fromkeys([u'的', u'，',u'\u3000','%',u'。',u'“',u'”',u'1',u'2',u'3',u'4',u'5',u'6',
                    u'7',u'8',u'9',u')',u'(',u'）',u'（',u'、',u'；',u'：',u"！",u"？",u"…",u"%",u"/",u"—"])
                    
wordlist=[]
for i in range(10,20):
    try:
        with open(dir_path+str(i)+".txt","r+") as f:
            text = f.read()
        li=[item for item in jieba.cut(text) if item not in stopwords]
        wordlist=wordlist+li
    except:
        pass
    
new_wordlist=list(set(wordlist))

word_counts = defaultdict(int)

for i in range(10,20):
    try:
        with open(dir_path+str(i)+".txt","r+") as f:
            text = f.read()
        li=[item for item in jieba.cut(text) if item not in stopwords]
        for i in range(len(new_wordlist)):
            if new_wordlist[i] in li:
                word_counts[new_wordlist[i]] +=1
    except:
        pass

word_idf = word_counts.copy()
for k in word_idf:
    word_idf[k]=word_idf[k]*1.0/10


for i in range(10,20):
        with open(dir_path+str(i)+".txt","r+") as f:
            text = f.read()
        li=[item for item in jieba.cut(text) if item not in stopwords]
        counts = Counter(li)
        words=counts.most_common()
        da=pd.DataFrame(words,columns=["words","counts"])
        total_sum=sum([words[item][1] for item in range(len(words))])
        total_sum=da['counts'].sum()
        ldf=[(words[j][1]*1.0/total_sum)/word_idf[words[j][0]] for j in range(len(words))]
        da['counts'] = ldf
        #name = [words[j][0].encode("gbk") for j in range(len(words))]#这两行改变words的编码
        #da['words']=name
        da2=da.sort_values('counts',ascending=False)
        #da2.to_csv(dir_path+str(i)+"_IDF.csv",index=False,header=False)
        da2.to_csv(dir_path+str(i)+"_IDF.txt",index=False,header=False,encoding="UTF-8")
        #da=pd.DataFrame(words,columns=["words","counts"])
        #da['counts'].sum()



###画个词云

text=[tuple(da.loc[i,]) for i in xrange(len(da2))]
wordcloud = WordCloud(font_path="D:\\Python\\Lib\\site-packages\\pytagcloud\\fonts\\MicrosoftYaHei.ttf").fit_words(text)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
