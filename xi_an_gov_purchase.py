from datetime import datetime
import requests
from lxml import etree
from defaults import region_guid

current_time = datetime.now()
current_date = current_time.strftime("%Y-%m-%d")
print("Current Time =", current_date)


def search_info(guid, time, info_list):
    url = "http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3&isgovertment="
    params = {'parameters[''title'']': '厨房',
              'parameters[''regionguid'']': guid,
              'parameters[''startdate'']': time,
              'parameters[''enddate'']': time
              }
    r = requests.post(url, params=params)
    content = r.content
    selector = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
    title = selector.xpath('//td/@title')
    link = selector.xpath("//td/a[@href]")
    for element2 in title:
        print(element2.attrib)


info_list = {}
for i, k in region_guid.items():
    # tuple 用数字来retrieve
    search_info(i, '2020-09-01', info_list)
