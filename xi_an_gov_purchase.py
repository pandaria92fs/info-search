import requests
from lxml import etree

url = "http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3&isgovertment="
params = {'parameters[''title'']': '厨房',
          'parameters[''regionguid'']': '6101'}
r = requests.post(url, params=params)
content = r.content
selector = etree.HTML(content)
title=selector.xpath('//title/text()')
print(str(title[0], 'utf-8'))
