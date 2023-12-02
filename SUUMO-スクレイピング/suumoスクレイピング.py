#!/usr/bin/env python
# coding: utf-8

# In[31]:


import requests
from bs4 import BeautifulSoup
import pandas as pd 
from retry import retry


# In[32]:


#目黒区
base_url = "https://suumo.jp/chintai/tokyo/sc_meguro/"


# In[33]:


@retry(tries=3, delay=10, backoff=2)
def get_html(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


# In[34]:


all_data = []
max_page = 10


# In[35]:


for page in range(1, max_page+1):
    url = base_url.format(page)


# In[36]:


soup = get_html(url)


# In[37]:


items = soup.findAll("div", {"class": "cassetteitem"})
print("page", page, "items", len(items))


# In[38]:


for item in items:
    stations = item.findAll("div", {"class": "cassetteitem_detail-text"})


# In[39]:


for station in stations:
    base_data = {}


# In[40]:


#基礎情報収集
base_data["名称"] = item.find("div", {"class": "cassetteitem_content-title"}).getText().strip()
base_data["カテゴリー"] = item.find("div", {"class": "cassetteitem_content-label"}).getText().strip()
base_data["アドレス"] = item.find("li", {"class": "cassetteitem_detail-col1"}).getText().strip()
base_data["アクセス"] = station.getText().strip()
base_data["築年数"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[0].getText().strip()
base_data["構造"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[1].getText().strip()


# In[41]:


tbodys = item.find("table", {"class": "cassetteitem_other"}).findAll("tbody")


# In[42]:


for tbody in tbodys:
    data = base_data.copy()

    data["階数"] = tbody.findAll("td")[2].getText().strip()

    data["家賃"] = tbody.findAll("td")[3].findAll("li")[0].getText().strip()
    data["管理費"] = tbody.findAll("td")[3].findAll("li")[1].getText().strip()

    data["敷金"] = tbody.findAll("td")[4].findAll("li")[0].getText().strip()
    data["礼金"] = tbody.findAll("td")[4].findAll("li")[1].getText().strip()

    data["間取り"] = tbody.findAll("td")[5].findAll("li")[0].getText().strip()
    data["面積"] = tbody.findAll("td")[5].findAll("li")[1].getText().strip()
                
    data["URL"] = "https://suumo.jp" + tbody.findAll("td")[8].find("a").get("href")
                
    all_data.append(data)


# In[43]:


df = pd.DataFrame(all_data)
df.to_csv("meguro_raw_data.csv")


# In[44]:


df


# In[ ]:




