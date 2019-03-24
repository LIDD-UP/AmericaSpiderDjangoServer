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

from spider_server.process_data import RealtorListPageMysqlsqlPipeline,RealtordetailPageMysqlPipeline
from spider_server.process_data import SpiderCloseProcess, RealtorListProcess
from AmericaSpiderDjangoServer.settings import spider_list_start_url,spider_detail_start_url,spider_detail_start_url2,spider_list_start_ur2



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def process_before_start_list_spider(request):
    realtor_process = RealtorListProcess(PYMYSQL_POOL)
    realtor_process.get_list_url()
    realtor_process.truncate_list_json_and_split_table()
    print("将list搜索条件插入redis里面，清空realtor_list_page_json 表和realtor_list_page_json_split 表成功")
    return HttpResponseRedirect('http://127.0.0.1:8000/spider_server/start_list_spider/')


def start_list_spider_requests_fn(url):
    requests.get(url)

def start_list_spider(request):
    print("启动列表页爬虫")
    spider_thread1 = threading.Thread(target=start_list_spider_requests_fn,args=(spider_list_start_url,))
    spider_thread1.start()
    # spider_thread2 = threading.Thread(target=start_list_spider_requests_fn, args=(spider_list_start_ur2,))
    # spider_thread2.start()
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
    data = request.body
    print(data)
    data_decode = data.decode()
    if data_decode is not None:
        close_spider_process = SpiderCloseProcess(PYMYSQL_POOL)
        close_spider_process.execute_spider_close()
    return HttpResponse("list json process successfully")


def start_detial_spider_requests_fn(url):
    requests.get(url=url)

# 详情页爬虫启动
def start_detail_spider(request):
    print("启动详情页爬虫")
    spider_thread1 = threading.Thread(target=start_detial_spider_requests_fn,args=(spider_detail_start_url,))
    spider_thread1.start()
    # spider_thread2 = threading.Thread(target=start_detial_spider_requests_fn, args=(spider_detail_start_url2,))
    # spider_thread2.start()
    return HttpResponse("execute successfully")


def detail_json_process(detail_data):
    print("详情页数据插入")
    time_now = time.time()
    data_loads = json.loads(detail_data)

    realtor_detail_test = RealtordetailPageMysqlPipeline(PYMYSQL_POOL)
    print("11")
    realtor_detail_test.traversal_json_data(data_loads)
    print("完成")
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




