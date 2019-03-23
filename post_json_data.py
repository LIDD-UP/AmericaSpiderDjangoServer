# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: post_json_data.py
@time: 2019/3/23
"""
import requests
import json

import time
# while True:
#     time_now = time.time()
req = requests.post(url='http://127.0.0.1:8000/spider_server/json_data_get_test/', data=json.dumps('{"aa":"11"}'))
    # print(req.text)
    # print(time.time()-time_now)


# data = '{"adafdaa":"1dsfdaf1","bdafab":"2dafdafasdf2"}'
# dict_a = {"aa":"11"}
# print(type(dict_a))
# data_json = json.dumps(data)
# data_dict = dict(json.loads(data_json))
# print(type(data_json)
#       )
# print(type(data_dict))


# j = '{"id": "007", "name": "007", "age": 28, "sex": "male", "phone": "13000000000", "email": "123@qq.com"}'
# l = '{"id": "007", "name": "007"}'
# k = '{"adafdaa":"1dsfdaf1","bdafab":"2dafdafasdf2"}'
# k_json = json.dumps(k)
# print(type(k_json))
# k_dict = json.loads(json.loads(k_json))
# print(type(k_dict))

# dict_a = json.loads(k)
# print(dict_a)
# print(type(dict_a))
