from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(1)
import json


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def process_before_start_list_spider(request):
    # realtor_process = RealtorListProcess(PYMYSQL_POOL)
    # realtor_process.get_list_url()
    # realtor_process.truncate_list_json_and_split_table()
    print("将list搜索条件插入redis里面，清空realtor_list_page_json 表和realtor_list_page_json_split 表成功")
    return HttpResponse("yes")


def start_list_spider_requests_fn(url):
    requests.get(url)

def start_list_spider(request):
    print("启动列表页爬虫")
    spider_thread1 = threading.Thread(target=start_list_spider_requests_fn,args=(spider_list_start_url,))
    spider_thread1.start()
    spider_thread2 = threading.Thread(target=start_list_spider_requests_fn, args=(spider_list_start_ur2,))
    spider_thread2.start()
    return HttpResponse("execute successfully")


def list_page_process_fn(list_data):
    # realtor_test_dict = RealtorListPageMysqlsqlPipeline(PYMYSQL_POOL)
    # realtor_test_dict.process_item(list_data)
    # print(request.get_json())
    pass


# 列表页数据的插入操作
def process_list_page_json(request):
    # app.app_context().push()
    # print(request.get_json())
    # json_data = request.get_json()
    # # executor.submit(list_page_process_fn,list_data=json_data)
    # list_json_process_thread = threading.Thread(target=list_page_process_fn,args=(json_data,))
    # list_json_process_thread.start()
    return HttpResponse("list page process success!")


# 列表页抓取完全之后的数据处理操作
def spider_close_process(request):
    # data = request.get_data()
    # print(data)
    # data_decode = data.decode()
    # if data_decode is not None:
    #     close_spider_process = SpiderCloseProcess(PYMYSQL_POOL)
    #     close_spider_process.execute_spider_close()
    return HttpResponse("list json process successfully")


def start_detial_spider_requests_fn(url):
    requests.get(url=url)

# 详情页爬虫启动
def start_detail_spider(request):
    print("启动详情页爬虫")
    spider_thread1 = threading.Thread(target=start_detial_spider_requests_fn,args=(spider_detail_start_url,))
    spider_thread1.start()
    spider_thread2 = threading.Thread(target=start_detial_spider_requests_fn, args=(spider_detail_start_url2,))
    spider_thread2.start()
    return HttpResponse("execute successfully")


def detail_json_process(detail_data):
    print("延迟测试10秒")
    # time.sleep(10)
    # realtor_detail_test = RealtordetailPageMysqlPipeline(PYMYSQL_POOL)
    # realtor_detail_test.traversal_json_data(detail_data)
    pass


# 详情页数据插入
def process_detail_page_json(request):
    # print(request.get_json())
    # json_data = request.get_json()
    # executor.submit(detail_json_process, detail_data=json_data)
    # detail_json_process_thread = threading.Thread(target=detail_json_process,args=(json_data,))
    # detail_json_process_thread.start()
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

    from spider_server.models import RealtorListJson
    RealtorListJson.objects.create(json_data='"aa":"bb"}')

    return HttpResponse(
        "test successful!!!!"
    )




