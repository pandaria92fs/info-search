# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 3:04 下午
# @Author  : burning_tomato
# @Site    : 
# @File    : second_part.py
# @Software: PyCharm
from datetime import datetime, timedelta

import requests
from lxml import etree

current_time = datetime.now()
current_date = current_time.strftime("%Y/%m/%d")
yesterday = datetime.now() + timedelta(days=-1)


def search_info(pageNo, keyword):
    # tuple 用数字来retrieve
    key_words = ["排烟", "厨", "炊具", "餐具", "酒店"]
    element_lst = []
    url = "http://www.yfbzb.com/search/invitedBidSearch"

    params = {
        'defaultSearch': 'false',
        'provinceId': 23,
        'pageSize': 100,
        'pageNo': pageNo,
        'keyword': keyword,
        'timeType': 0
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 ',

        'Host': 'www.yfbzb.com',
        'Upgrade - Insecure - Requests': '1',

        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

        'Accept - Encoding': 'gzip, deflate',
        'Connection': 'keep - alive'
    }
    r = requests.get(url, headers=headers, params=params).text
    # content = r.content
    selector = etree.HTML(r)
    raw_titles = selector.xpath('//tr/td/a')
    title_times = selector.xpath('//tr/td[contains(text(),"2020")]/text()')
    link = selector.xpath('//tr/td/a/@href')
    element_lst = []
    for i in range(0, len(raw_titles) - 1):
        if str(title_times[i]) == current_date or str(title_times[i]) == yesterday.strftime("%Y/%m/%d"):
            title = raw_titles[i].xpath("string(.)")
            dict_val = {"标题": title, "链接": "http://www.yfbzb.com/" + link[i], "信息发布日期": title_times[i], "信息来源网站": "乙方宝"}
            element_lst.append(dict_val)
    if title_times[-1] is current_date:
        pageNo += 1
        search_info(pageNo, keyword)
    return element_lst


def run():
    lst = []
    key_words = ["排烟", "厨", "炊具", "餐具", "酒店"]
    for key in key_words:
        lst.append(search_info(1, key))
    return lst


run()
