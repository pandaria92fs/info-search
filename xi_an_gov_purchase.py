import requests
from lxml import etree

url = "http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3&isgovertment="
params = {'parameters[''title'']': '厨房',
          'parameters[''regionguid'']': '6101'}
r = requests.post(url, params=params)
content = r.content
selector = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
title = selector.xpath('//td[@title]')
for element in title:
    print(element.attrib)
