# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: batch_insert_to_redis.py
@time: 2019/3/25
"""
import redis
import redis
import pandas as pd
import time

# redis_pool.lpush("realtor:test","dajlfdkaj")
server_root_path= r'F:\PycharmProject\AmericaSpiderDjangoServer'
# server_root_path = r'/usr/project/AmericaSpiderDjangoServer'
realtor_list_search_criteria = list(set(list(pd.read_csv(server_root_path + r'/tools/realtor_app_list_page_search_criteria.csv')['countyStateJoin'])))


# sadd：是针对redis中set类型数据进行插入
# 如果你的redis数据是list类型那么使用lpush 或者 rpush
time_now = time.time()
pool = redis.ConnectionPool(
                            # host='106.12.196.86',
                            # host='127.0.0.1',
                            # host = '138.197.143.39',
                            host= '106.12.196.106'
                            # password='123456'
                            )
r = redis.Redis(connection_pool=pool)
with r.pipeline() as p:
    for index, result in enumerate(realtor_list_search_criteria):
        p.lpush("realtor:list_url", result)
    p.execute()
#
print("详情页搜索条件插入redis花费时间{}s".format(time.time() - time_now))