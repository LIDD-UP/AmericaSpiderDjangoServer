from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(1)
import json
from spider_server.models import RealtorListPageJson,RealtorDetailJson
from spider_server.process_data import RealtorListProcess
from AmericaSpiderDjangoServer.settings import PYMYSQL_POOL
from AmericaSpiderDjangoServer.settings import redirect_start_list_spider_url
import redis

from spider_server.process_data import RealtorListPageMysqlsqlPipeline,RealtordetailPageMysqlPipeline
from spider_server.process_data import SpiderCloseProcess, RealtorListProcess
from AmericaSpiderDjangoServer.settings import spider_list_start_url,spider_detail_start_url,spider_detail_start_url2,spider_list_start_ur2,spider_list_start_ur3,spider_detail_start_url3
from spider_server.process_data import GetListSearchCriteria,GetDetailSearchCriteria
from AmericaSpiderDjangoServer.settings import redis_pool


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def process_before_start_list_spider(request):

    realtor_process = RealtorListProcess(PYMYSQL_POOL)
    #print('直接一次性将搜索条件插入')
    # realtor_process.get_list_url()
    realtor_process.truncate_list_json_and_split_table()

    # 激活爬虫 爬虫端作为请求端的做法；会出现丢数据的情况；
    get_list_url = GetListSearchCriteria()
    get_list_url.get_list_url()

    print("清空realtor_list_page_json 表和realtor_list_page_json_split 表成功")
    return HttpResponseRedirect(redirect_start_list_spider_url)
    # return HttpResponse('处理成功')


# def get_list_search_criteria_fn():
#     get_list_url = GetListSearchCriteria()
#     get_list_url.get_list_url()


def get_list_search_criteria(request):
    get_list_url = GetListSearchCriteria()
    print(GetListSearchCriteria.offset)
    print(GetListSearchCriteria.realtor_list_search_criteria_len)
    if GetListSearchCriteria.offset == GetListSearchCriteria.realtor_list_search_criteria_len:
        return HttpResponse("list页搜索条件已经空了")
    get_list_url.get_list_url()
    # thread1 = threading.Thread(target=get_list_search_criteria_fn)
    # thread1.start()
    return HttpResponse("获取list数据插入redis成功")


def start_list_spider_requests_fn(url):
    requests.get(url)


def start_list_spider(request):
    print("启动列表页爬虫")
    spider_thread1 = threading.Thread(target=start_list_spider_requests_fn,args=(spider_list_start_url,))
    spider_thread1.start()
    # spider_thread2 = threading.Thread(target=start_list_spider_requests_fn, args=(spider_list_start_ur2,))
    # spider_thread2.start()
    # spider_thread3 = threading.Thread(target=start_list_spider_requests_fn, args=(spider_list_start_ur3,))
    # spider_thread3.start()
    return HttpResponse("execute successfully")


def list_page_process_fn(list_data):
    print('列表页数据插入')
    data_loads = json.loads(list_data)
    print(type(data_loads))
    json_dict = json.loads(data_loads)

    bulk_insert_data = list()
    for item_data in json_dict["data"]:
        json_dict_houses = item_data['listings']
        bulk_insert_data += [RealtorListPageJson(json_data=json.dumps(house)) for house in json_dict_houses]
    print("list table 插入成功，批量插入了{}条".format(len(bulk_insert_data)))
    RealtorListPageJson.objects.bulk_create(bulk_insert_data)


# 列表页数据的插入操作
def process_list_page_json(request):
    row_data = request.body
    executor.submit(list_page_process_fn,list_data=row_data)
    return HttpResponse("服务器已经接受到了list json  存储处理请求")


# 列表页抓取完全之后的数据处理操作
def spider_close_process(request):

    close_spider_process = SpiderCloseProcess(PYMYSQL_POOL)
    close_spider_process.execute_spider_close()

    # 用于激活详情页爬虫，当不是将所有的搜索条件插入redis里面的时候
    get_detail_url = GetDetailSearchCriteria()
    get_detail_url.get_detail_url()

    return HttpResponse("list json process successfully")


# def get_detail_search_criteria_fn():
#     get_detail_url = GetDetailSearchCriteria()
#     get_detail_url.get_detail_url()


def get_detail_search_criteria(request):
    get_detail_url = GetDetailSearchCriteria()
    if get_detail_url.offset == get_detail_url.realtor_detail_json_query_result_len:
        return HttpResponse("detail搜索条件已经空了")
    get_detail_url.get_detail_url()
    # thread1 = threading.Thread(target=get_detail_search_criteria_fn)
    # thread1.start()
    return HttpResponse("获取detail数据插入redis成功")


def start_detial_spider_requests_fn(url):
    requests.get(url=url)


# 详情页爬虫启动
def start_detail_spider(request):
    print("启动详情页爬虫")
    spider_thread1 = threading.Thread(target=start_detial_spider_requests_fn, args=(spider_detail_start_url,))
    spider_thread1.start()
    # spider_thread2 = threading.Thread(target=start_detial_spider_requests_fn, args=(spider_detail_start_url2,))
    # spider_thread2.start()
    # spider_thread3 = threading.Thread(target=start_detial_spider_requests_fn, args=(spider_detail_start_url3,))
    # spider_thread3.start()
    return HttpResponse("execute successfully")


def detail_json_process(detail_data):
    print("详情页数据插入")
    time_now = time.time()
    data_loads = json.loads(detail_data)
    realtor_detail_test = RealtordetailPageMysqlPipeline(PYMYSQL_POOL)
    realtor_detail_test.traversal_json_data(data_loads)
    # for format_data in json_dict['data']:
    #     RealtorDetailJson.objects.filter(property_id=format_data['propertyId']).update(detail_json=json.dumps(format_data['detailJson']))
    print("detail 表跟新花费时间{}s".format(time.time()-time_now))


# 详情页数据插入
def process_detail_page_json(request):
    row_data = request.body
    executor.submit(detail_json_process, detail_data=row_data)
    return HttpResponse("detail json process success!")


def async_test(request):
    print("数据处理开始")
    time.sleep(10)
    print("数据处理结束")


def json_data_get_test(request):
    # print(request.method)
    # # print(request.body)
    # # data = json.dumps(request.post['json'])
    # # print(type(request.data))
    # print(type(request.body))
    # data = request.body
    # # data = data_byte.decode()
    # data_dict = (json.loads(data))
    # print(type(data_dict))
    # data_dict2 = json.loads(data_dict)
    # print(type(data_dict2))
    # for i in range(10):
    #     data_dict2 = json.loads(data_dict2)
    #     print(type(data_dict2))

    # print(data_dict)
    # print(type(data_dict))
    # print(data_dict.keys())
    # print(data_dict['aa'])
    # data_dict = json.loads(data)
    # print(data_dict)
    return HttpResponse(
        "test successful!!!!"
    )


# 服务器端主动监听redis 为爬虫端喂养爬取数据
# def judge_redis_is_empty():
#     while True:
#         try:
#             list_count = redis_pool.llen('realtor:list_url')
#             print("redis中list搜索条件个数:",list_count)
#             if list_count==0:
#                 req = requests.get(url='http://127.0.0.1:8000/spider_server/get_list_search_criteria/')
#                 print(req.text)
#                 if req.text=='list页搜索条件已经空了':
#                     time.sleep(20)
#                     requests.get(url='http://127.0.0.1:8000/spider_server/spider_close_process/')
#                     requests.get(url='http://127.0.0.1:8000/spider_server/start_detail_spider/')
#                     while True:
#                         detail_count = redis_pool.llen('realtor:property_id')
#                         if detail_count == 0:
#                             req2 = requests.get(url='http://127.0.0.1:8000/spider_server/get_detail_search_criteria/')
#                             if req2.text=='detail搜索条件已经空了':
#                                 break
#         except Exception as e:
#             print(e)
#             continue
#
#
#
#
# judge_redis_is_empty_thread = threading.Thread(target=judge_redis_is_empty)
# judge_redis_is_empty_thread.start()



