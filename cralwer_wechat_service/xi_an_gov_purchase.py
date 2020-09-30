from datetime import datetime, timedelta
import requests
from lxml import etree
from lxml.html import fromstring, tostring

current_time = datetime.now()
current_date = current_time.strftime("%Y-%m-%d")
yesterday = datetime.now() + timedelta(days=-1)
print("Current Time =", current_date)
print(yesterday)

region_guid = {
    610001: "陕西省本省",
    6101: "西安市",
    6102: "铜川市",
    6103: "宝鸡市",
    6104: "咸阳市",
    6105: "渭南市",
    6106: "延安市",
    6107: "汉中市",
    6108: "榆林市",
    6109: "安康市",
    6110: "商洛市",
    6111: "杨凌示范区",
    6169: "西咸新区"
}


def search_info(time):
    element_lst = []
    for i, k in region_guid.items():
        # tuple 用数字来retrieve
        key_words = ["排烟", "系统改造", "厨", "炊具", "酒店"]
        # print(yesterday.strftime("%Y-%m-%d"))
        url = "http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3&isgovertment="
        params = {'parameters[''title'']': '',
                  'parameters[''regionguid'']': i,
                  'parameters[''startdate'']': yesterday.strftime("%Y-%m-%d"),
                  'parameters[''enddate'']': time
                  }
        r = requests.post(url, params=params)
        content = r.content
        selector = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        title = [str(s) for s in selector.xpath('//td/@title')]
        link = selector.xpath("//td/a[@href]")
        print(title)
        for t, l in zip(title, link):
            for key in key_words:
                if key in t:
                    dict_val = {"标题": t, "链接": l.attrib["href"], "信息爬取日期": time}
                    element_lst.append(dict_val)
    return element_lst


info_list = []
info_list = search_info(current_date)

print(info_list)
