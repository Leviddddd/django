import hashlib
import time
import json
import requests
import urllib3
import numpy as np

urllib3.disable_warnings()
addr = 'https://api.wonder.net.cn'
test_url = 'https://test6.wonder.net.cn'
local_url = 'https://test4.wonder.net.cn'
key = "daylong@168."
ios = 'ios'
android_key = 'fa8e831ed99f25503738e61f239daf32'


class Request(object):
    def __init__(self):
        self.data = None  # 用例数据
        self.params = None  # 请求参数
        self.json_str = None  # 请求参数转为字符串
        self.header = None  # 请求头部
        self.header_md5 = None  # 请求头部md5加密
        self.daylongPas = None  # md5加密公式
        self.timestamp = None  # 时间戳
        self.response = None  # 请求实例化
        self.header_print = None  # 请求头部
        self.response_json = None  # 响应报文
        self.url = None  # 请求地址
        self.way = None  # 请求方式
        self.unit = None  # 所属模块

    # md5加密
    def md5(self, platform, jsons):
        # 请求参数json格式转str格式
        self.json_str = json.dumps(jsons)
        # 加密实例化
        self.daylongPas = hashlib.md5()
        # 时间戳
        self.timestamp = str(int(time.time() * 1000))
        # md5加密公式
        self.daylongPas.update(self.timestamp.encode(encoding='unicode_escape') + '+'.encode(encoding='unicode_escape')
                               + key.encode(encoding='unicode_escape') + '+'.encode(encoding='unicode_escape')
                               + self.json_str.encode(encoding='unicode_escape') + '+'.encode(encoding='unicode_escape')
                               + platform.encode(encoding='unicode_escape'))
        # 头部md5加密格式
        self.header_md5 = {'timestamp': self.timestamp, 'platform': platform,
                           'daylongPas': self.daylongPas.hexdigest(),
                           'jsonStr': self.json_str}
        # 返回加密后的实例
        return self.header_md5

    # post请求
    def post(self, url, param, platform):
        self.url = url
        self.params = param
        try:
            # post请求头部加密json
            self.header = self.md5(platform, self.params)
            # 调用requests库post请求实例化
            self.response = requests.post(url=self.url, json=self.params, headers=self.header, verify=False)
            return self.response
        except Exception as e:
            return e

    # get请求
    def get(self, url, params, **kwargs):
        self.url = url
        self.params = params
        # 判断参数是否为NAN（excel中是否为空）
        if isinstance(self.params, float):
            try:
                # 调用requests库的get请求实例化
                self.response = requests.get(url=self.url, verify=False)
                # 返回实例响应json格式
                return self.response
            except Exception as e:
                return e
        else:
            # 请求参数json
            # self.params = eval(params)
            try:
                # 调用requests库的get请求实例化
                self.response = requests.get(url=self.url, params=self.params, verify=False)
                # 返回实例响应json格式
                return self.response
            except Exception as e:
                return e


if __name__ == '__main__':
    res = Request()
    token_login_api = '/login/token_login'
    login_param = {
        'loginWayType': 2,
        'loginStr': 139986,
        'password': 'a31248719'
    }
    # login = res.post(addr+token_login_api, login_param, 'ios')
    # user_token = login.json()['data']['accessToken']
    # print(user_token)
    slot_param = dict(slotsStr="H,H,H,A,B,A,B,I,K", isRobMoney=0)
    slot_api = '/peripheral/slots_brocast_test'
    response = res.get(test_url+slot_api, slot_param)


