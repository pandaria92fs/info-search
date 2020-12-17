# -*- coding: utf-8 -*-
import requests
import lxml.etree
from datetime import datetime, timedelta

current_time = datetime.now()
current_date = current_time.strftime("%Y-%m-%d")
yesterday = datetime.now() + timedelta(days=-1)

url = "https://www.plap.cn/index/selectsumBynews.html?id=3&twoid=24&title=%25E5%258E%25A8%25E6%2588%25BF&productType=&productTypeName=&tab=%25E7%2589%25A9%25E8%25B5%2584&lastArticleTypeName=&publishStartDate=&publishEndDate="


def pla_purchase():
    r = requests.get(url)
    content=r.content
    selector = lxml.etree.HTML(content, parser=lxml.etree.HTMLParser(encoding='utf-8'))
    print(selector.xpath("//li/a[@title] ")[3].xpath('string()'))

pla_purchase()
