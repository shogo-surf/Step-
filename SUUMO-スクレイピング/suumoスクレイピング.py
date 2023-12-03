#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd 
from retry import retry


#目黒区
base_url = "https://suumo.jp/chintai/tokyo/sc_meguro/"


@retry(tries=3, delay=10, backoff=2)
def get_html(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


all_data = []
max_page = 10



for page in range(1, max_page+1):
    url = base_url.format(page)
    soup = get_html(url)
    items = soup.findAll("div", {"class": "cassetteitem"})
    print("page", page, "items", len(items))
    for item in items:
        stations = item.findAll("div", {"class": "cassetteitem_detail-text"})
        for station in stations:
            base_data = {}
            base_data["名称"] = item.find("div", {"class": "cassetteitem_content-title"}).getText().strip()
            base_data["カテゴリー"] = item.find("div", {"class": "cassetteitem_content-label"}).getText().strip()
            base_data["アドレス"] = item.find("li", {"class": "cassetteitem_detail-col1"}).getText().strip()
            base_data["アクセス"] = station.getText().strip()
            base_data["築年数"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[0].getText().strip()
            base_data["構造"] = item.find("li", {"class": "cassetteitem_detail-col3"}).findAll("div")[1].getText().strip()

            tbodys = item.find("table", {"class": "cassetteitem_other"}).findAll("tbody")
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

df = pd.DataFrame(all_data)
df.to_csv("meguro_raw_data.csv")
