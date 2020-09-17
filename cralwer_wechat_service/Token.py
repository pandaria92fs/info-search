import requests
import json
from cralwer_wechat_service.const import corp_id, secret


def get_token():
    URL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corp_id + "&corpsecret=" + secret
    Token = requests.get(URL).json()
    return Token["access_token"]


