# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: te_post.py
@time: 2019/3/15
"""
import requests
import json
import os


# test list
# requests.post('http://127.0.0.1:5000/process_list_page_json/',
#               json='''{"data":[{"listings":[{"property_id":"5528101208","listing_id":"652373674","prop_type":"condo","last_update":"2019-03-14T11:32:02Z","rdc_web_url":"https://www.realtor.com/realestateandhomes-detail/8253-Highway-98-D200_Navarre_FL_32566_M55281-01208","prop_sub_type":"condo","is_turbo":false,"address":"8253 Highway 98 Unit D200, Navarre, 32566","prop_status":"for_sale","price_raw":220000,"sqft_raw":1146,"list_date":"2019-03-14T11:40:37Z","office_name":"Re/Max Gulf Properties","products":["co_broke","basic_opt_in","co_broke"],"is_showcase":false,"price":"$220,000","beds":2,"baths":3,"sqft":"1,146 sq ft","lot_size":"1,307 sq ft lot","photo":"https://ap.rdcpix.com/1756448895/05fb1701ebdb475d2fa6e46f4bec2305l-m0x.jpg","is_cobroker":true,"short_price":"$220K","baths_half":1,"baths_full":2,"photo_count":25,"lat":30.4272976,"lon":-86.88539,"is_new_listing":true,"has_leadform":true,"page_no":1,"rank":1,"list_tracking":"type|property|data|prop_id|5528101208|list_id|652373674|page|rank|list_branding|listing_agent|listing_office|property_status|product_code|advantage_code^1|1|0|1|35T|9HU|0^^$0|1|2|$3|4|5|6|7|F|8|G|9|$A|H|B|I]|C|J|D|K|E|L]]"},{"property_id":"6049007396","listing_id":"652370298","prop_type":"single_family","last_update":"2019-03-13T22:28:13Z","rdc_web_url":"https://www.realtor.com/realestateandhomes-detail/2027-Heritage-Park-Way_Navarre_FL_32566_M60490-07396","is_turbo":false,"address":"2027 Heritage Park Way in Heritage Park, Navarre, 32566","prop_status":"for_sale","price_raw":415000,"sqft_raw":2676,"list_date":"2019-03-14T03:35:52Z","office_name":"Keller Williams Realty Navarre","products":["co_broke","basic_opt_in","co_broke"],"is_showcase":false,"price":"$415,000","beds":4,"baths":3,"sqft":"2,676 sq ft","lot_size":"0.26 acres","photo":"https://ap.rdcpix.com/694472650/cf1c33ba89af42adfd4bdb401dc8ca24l-m0x.jpg","is_cobroker":true,"short_price":"$415K","baths_full":3,"photo_count":63,"lat":30.407241,"lon":-86.840354,"is_new_listing":true,"has_leadform":true,"page_no":1,"rank":2,"list_tracking":"type|property|data|prop_id|6049007396|list_id|652370298|page|rank|list_branding|listing_agent|listing_office|property_status|product_code|advantage_code^1|2|0|1|35T|9HU|0^^$0|1|2|$3|4|5|6|7|F|8|G|9|$A|H|B|I]|C|J|D|K|E|L]]"}]},{"listings":[{"property_id":"5528101208","listing_id":"652373674","prop_type":"condo","last_update":"2019-03-14T11:32:02Z","rdc_web_url":"https://www.realtor.com/realestateandhomes-detail/8253-Highway-98-D200_Navarre_FL_32566_M55281-01208","prop_sub_type":"condo","is_turbo":false,"address":"8253 Highway 98 Unit D200, Navarre, 32566","prop_status":"for_sale","price_raw":220000,"sqft_raw":1146,"list_date":"2019-03-14T11:40:37Z","office_name":"Re/Max Gulf Properties","products":["co_broke","basic_opt_in","co_broke"],"is_showcase":false,"price":"$220,000","beds":2,"baths":3,"sqft":"1,146 sq ft","lot_size":"1,307 sq ft lot","photo":"https://ap.rdcpix.com/1756448895/05fb1701ebdb475d2fa6e46f4bec2305l-m0x.jpg","is_cobroker":true,"short_price":"$220K","baths_half":1,"baths_full":2,"photo_count":25,"lat":30.4272976,"lon":-86.88539,"is_new_listing":true,"has_leadform":true,"page_no":1,"rank":1,"list_tracking":"type|property|data|prop_id|5528101208|list_id|652373674|page|rank|list_branding|listing_agent|listing_office|property_status|product_code|advantage_code^1|1|0|1|35T|9HU|0^^$0|1|2|$3|4|5|6|7|F|8|G|9|$A|H|B|I]|C|J|D|K|E|L]]"},{"property_id":"6049007396","listing_id":"652370298","prop_type":"single_family","last_update":"2019-03-13T22:28:13Z","rdc_web_url":"https://www.realtor.com/realestateandhomes-detail/2027-Heritage-Park-Way_Navarre_FL_32566_M60490-07396","is_turbo":false,"address":"2027 Heritage Park Way in Heritage Park, Navarre, 32566","prop_status":"for_sale","price_raw":415000,"sqft_raw":2676,"list_date":"2019-03-14T03:35:52Z","office_name":"Keller Williams Realty Navarre","products":["co_broke","basic_opt_in","co_broke"],"is_showcase":false,"price":"$415,000","beds":4,"baths":3,"sqft":"2,676 sq ft","lot_size":"0.26 acres","photo":"https://ap.rdcpix.com/694472650/cf1c33ba89af42adfd4bdb401dc8ca24l-m0x.jpg","is_cobroker":true,"short_price":"$415K","baths_full":3,"photo_count":63,"lat":30.407241,"lon":-86.840354,"is_new_listing":true,"has_leadform":true,"page_no":1,"rank":2,"list_tracking":"type|property|data|prop_id|6049007396|list_id|652370298|page|rank|list_branding|listing_agent|listing_office|property_status|product_code|advantage_code^1|2|0|1|35T|9HU|0^^$0|1|2|$3|4|5|6|7|F|8|G|9|$A|H|B|I]|C|J|D|K|E|L]]"}]}]}'''
#               )


# test detail
# item_data = json.dumps({"data": [{"detailJson": '{"11":"123"}', "propertyId": 123445678},
#                                  {"detailJson": '{"11":"123"}', "propertyId": 123445678}]})
#
#
# req = requests.post('http://127.0.0.1:5000/process_detail_page_json/',
#               json=item_data
#               )


# print(req.text)

# import os
# import sys
# sys.path.append("F:\PycharmProject\AmericanRealEstate")
# os.chdir("F:\PycharmProject\AmericanRealEstate")
#
# os.system(r"python {}".format(detial_spider_main_path))


# requests.get(url='http://138.197.143.39:5000/process_before_start_list_spider/')


# requests.post(url='http://127.0.0.1:5000/spider_close_process/' , data="list_spider_close")

# while True:
# req = requests.post(url='http://138.197.143.39:5000/process_detail_page_json/',json='{"aa":"11"}')

import time
# while True:
#     time_now = time.time()
#     req = requests.post(url='http://138.197.143.39:5000/process_detail_page_json/', json=json.dumps('{"aa":"11"}'))
#     # print(req.text)
#     print(time.time()-time_now)


# req = requests.get(url='http://127.0.0.1:8000/spider_server/spider_close_process/',data='yes')
# print(req.text)

from AmericaSpiderDjangoServer.settings import PYMYSQL_POOL

# conn = PYMYSQL_POOL.connection()
# print(conn)
# from spider_server.process_data import RealtordetailPageMysqlPipeline
# realtor_detail_test = RealtordetailPageMysqlPipeline(PYMYSQL_POOL)
# print("11")
# data ='{"aa":"bb"}'
#
# realtor_detail_test.traversal_json_data(data)

# print("请求结束")

import pandas as pd
import redis
pool = redis.ConnectionPool(
                            # host='106.12.196.86',
                            # host='127.0.0.1',
                            # host = '138.197.143.39',
                            host= '106.12.196.106'
                            # password='123456'
                            )
redis_pool = redis.Redis(connection_pool=pool)
redis_pool.flushdb()
# server_root_path= r'F:\PycharmProject\AmericaSpiderDjangoServer'
server_root_path = r'/usr/project/AmericaSpiderDjangoServer'
realtor_list_search_criteria = list(set(list(pd.read_csv(server_root_path + r'/tools/realtor_app_list_page_search_criteria.csv')['countyStateJoin'])))

print(len(realtor_list_search_criteria))
time_now = time.time()
for index,result in enumerate(realtor_list_search_criteria):
    print(index)
    redis_pool.lpush('realtor:list_url',result)

print("详情页搜索条件插入redis花费时间{}s".format(time.time() - time_now))


list_property_id_list = []
random_list = []