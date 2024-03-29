#!/usr/bin/env python
# coding: utf-8

# In[1]:


word2info = {}
import glob
filenames = glob.glob('./词典七类/*txt') 
for filename in filenames:
    name = filename.split('\\')[-1].split('.')[0]
    with open(filename, encoding='utf-8') as fr:
        for line in fr:
            word2info.setdefault(name, []).append(line.strip())


# In[2]:


ALLKEYS = []
for ls in word2info.values():
    ALLKEYS.extend(ls)


# In[3]:


ALLKEYS = set(ls)


# In[4]:


word2info.keys()


# In[5]:


import numpy as np
from collections import defaultdict
def getData(datas):
    label2num = defaultdict(int)
    num = 1 #总情感词数
    for k, v in word2info.items():
        for _ in v:
            if _ in ''.join(datas):
                num+=1
                label2num[k] = label2num.setdefault(k, 0) +1
            else:
                pass
    emos = ['乐','好','怒','衰','惧','恶','惊']
    ifos = label2num['乐'], label2num['好'], label2num['怒'], label2num['衰'], label2num['惧'], label2num['恶'], label2num['惊']
    return datas, label2num['乐'], label2num['好'], label2num['怒'], label2num['衰'], label2num['惧'], label2num['恶'], label2num['惊'], emos[np.argmax(ifos)]


# In[6]:


import pandas as pd


# In[7]:


df = pd.read_csv('文本去重汇总.csv', encoding='utf-8')


# In[8]:


df.head()


# In[9]:


import csv
fw = open('results.csv', 'w',encoding='utf-8', newline='')
csv_writer = csv.writer(fw)
tts = '内容	乐的占比 	好的占比	怒的占比	哀的占比	惧的占比 	恶的占比	惊的占比	标签'
csv_writer.writerow([x for x in tts.split()])
from tqdm import tqdm
for filename in tqdm(df['内容'].values):
    info = getData(filename)
    csv_writer.writerow(list(info))
fw.close()


# In[10]:


dfx = pd.read_csv('results.csv')


# In[11]:


dfx.head()


# In[12]:


label2info = {}
for l in dfx['标签']:
    label2info[l] = label2info.setdefault(l, 0) + 1


# In[13]:


label2info


# In[14]:


from pyecharts import options as opts
from pyecharts.charts import Page, Pie
l1 = []
num = []
for k, v in label2info.items():
    l1.append(k)
    num.append(v)
c = (
        Pie()
        .add("", [list(z) for z in zip(l1,num)])
        .set_global_opts(title_opts=opts.TitleOpts(title="细粒度情感占比"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
c.render_notebook()


# In[15]:


dfx.to_excel('final_results.xlsx', index=False)


# In[ ]:




