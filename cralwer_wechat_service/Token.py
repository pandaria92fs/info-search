# -*- coding: utf-8 -*-
import datetime
import json
import time

import requests

import second_part
import shan_xi_gov_purchase as shan_xi_gov
import xi_an_gov_purchase as xi_an_gov
from time import sleep


class WeChat:
    def __init__(self):
        self.CORPID = 'wwc7a16e080c15cbe3'  # 企业ID，在管理后台获取
        self.CORPSECRET = 'tLua3vWd3yDTvEfUUnJU7zZJMUWhpql28-h_P9DekhY'  # 自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = '1000002'  # 应用ID，在后台应用中获取
        self.TOPARTY = '2'  # 接收者用户名,多个用户用|分割

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        try:
            with open('/root/info-search/cralwer_wechat_service/tmp/access_token.conf',
                      'r') as f:
                t, access_token = f.read().split()
        except:
            with open('/root/info-search/cralwer_wechat_service/tmp/access_token.conf',
                      'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open(
                        '/root/info-search/cralwer_wechat_service/tmp/access_token.conf',
                        'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "toparty": self.TOPARTY,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        response = requests.post(send_url, send_msges)
        response = response.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return response["errmsg"]


# Python program to convert a list to string

# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1


def determent_second(list):
    flag = False
    for i in list:
        if len(i) is not 0:
            flag = True
    return flag


key_words = ["排烟", "厨", "炊具", "餐具", "酒店"]

if __name__ == '__main__':
    wx = WeChat()
    xi_an_gov_info_list = xi_an_gov.info_list
    shan_xi_gov_info_list = shan_xi_gov.search_info(shan_xi_gov.current_date)
    second_part_list = second_part.run()
    info_list = xi_an_gov_info_list + shan_xi_gov_info_list
    wx.send_data("早上好！😊现在是" + datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))
    sleep(1)
    if info_list:
        wx.send_data(
            "这是今天爬取到的信息！这是正式版信息！请注意关注！")
        wx.send_data(str(info_list) + "\n" + "昨天已经推送过的消息注意重复信息！！！\n")
        sleep(1)
    else:
        wx.send_data("今日政府采购没有关于厨房,炊具,酒店,食堂,厨具的关键词消息推送\n ")
        sleep(1)

    wx.send_data("以下推送来自于乙方宝，请持续关注！ ")
    sleep(1)
    if determent_second(second_part_list):
        for i in range(0, len(second_part_list) - 1):
            if len(second_part_list[i]) is not 0:
                wx.send_data(
                    "这是今天爬取到的乙方宝信息！这是正式版信息！请注意关注！")
                wx.send_data(str(second_part_list[i]) + "昨天已经推送过的消息注意重复信息！！！\n")
                sleep(1)
            else:
                wx.send_data(
                    "关键词：" + key_words[i] + "结果为空！")
                sleep(1)
    else:
        wx.send_data("今日乙方宝没有关于厨房,炊具,酒店,食堂,厨具的关键词消息推送 ")
        sleep(1)

    wx.send_data("以上就是今天的全部!拜拜👋～\n")
    sleep(1)
