# -*-coding= utf-8 -*-
# @Time: 2020/11/8 9:25
# @Author: XianHui chen
# @File: shan_xi_gov_purchase.py
# @Software:PyCharm
# @description:山西采购与招标
from datetime import datetime, timedelta
import requests
from lxml import etree, html
from lxml.html import fromstring, tostring, HTMLParser

current_time = datetime.now()
current_date = current_time.strftime("%Y-%m-%d")
yesterday = datetime.now() + timedelta(days=-1)


def search_info(time):
    # tuple 用数字来retrieve
    key_words = ["空港"]
    # print(yesterday.strftime("%Y-%m-%d"))
    element_lst = []
    url = "http://bulletin.sntba.com/xxfbcmses/search/bulletin.html"
    params = {
        'parameters[''categoryId'']': 88,
        'parameters[''searchDate'']': "1995-11-08",
        'parameters[''dates'']': "300",
        'parameters[''startcheckDate'']': yesterday.strftime("%Y-%m-%d"),
        'parameters[''endcheckDate'']': time
    }
    r = requests.post(url, params=params)
    content = r.content
    selector = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
    title = [s for s in selector.xpath('//tr/td/a/@title')]
    # print(html.tostring(title[0], encoding='utf-8').encode())
    link = selector.xpath("//tr/td/a/@href")
    for t, l in zip(title, link):
        for key in key_words:
            if key in t:
                dict_val = {"标题": t, "链接": l, "信息爬取日期": time, "信息来源网站": "陕西采购与招标网"}
                element_lst.append(dict_val)
    return element_lst


print(search_info(current_time))
