from datetime import datetime
import requests
from lxml import etree
from defaults import region_guid

current_time = datetime.now()
current_date = current_time.strftime("%Y-%m-%d")
print("Current Time =", current_date)


def search_info(time):
    element_lst = []
    for i, k in region_guid.items():
        # tuple 用数字来retrieve
        print(i, k)
        url = "http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3&isgovertment="
        params = {'parameters[''title'']': '',
                  'parameters[''regionguid'']': i,
                  'parameters[''startdate'']': time,
                  'parameters[''enddate'']': time
                  }
        r = requests.post(url, params=params)
        content = r.content
        selector = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        title = selector.xpath('//td/@title')
        link = selector.xpath("//td/a[@href]")
        print(title)
        for t, l in zip(title, link):
            dict_val = {"标题": t, "链接": l.attrib["href"], "日期": time}
            element_lst.append(dict_val)
    return element_lst


info_list = []
info_list = search_info(current_date)
print(info_list)
