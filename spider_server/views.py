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
from AmericaSpiderDjangoServer.settings import PYMYSQL_POOL
from AmericaSpiderDjangoServer.settings import redirect_start_list_spider_url
from AmericaSpiderDjangoServer.settings import SPIDER_CLIENT_NUMBER
import redis
import zlib

from spider_server.process_data import RealtorListPageMysqlsqlPipeline,RealtordetailPageMysqlPipeline
from spider_server.process_data import SpiderCloseProcess, RealtorListProcess
from AmericaSpiderDjangoServer.settings import spider_list_start_url,spider_detail_start_url,spider_detail_start_url2,spider_list_start_ur2,spider_list_start_ur3,spider_detail_start_url3
from AmericaSpiderDjangoServer.settings import redirect_post_detail_criteria_to_client_url
from spider_server.process_data import PostDetailSearchCriteriaToClient


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def process_before_start_list_spider(request):

    realtor_process = RealtorListProcess(PYMYSQL_POOL)

    realtor_process.truncate_list_json_and_split_table()

    print("清空realtor_list_page_json 表和realtor_list_page_json_split 表成功")
    return HttpResponseRedirect(redirect_start_list_spider_url)
    # return HttpResponse('处理成功')


def start_list_spider_requests_fn(url):
    requests.get(url)


def start_list_spider(request):
    print("启动列表页爬虫")
    if SPIDER_CLIENT_NUMBER == 1:
        spider_thread1 = threading.Thread(target=start_list_spider_requests_fn,args=(spider_list_start_url,))
        spider_thread1.start()
    if SPIDER_CLIENT_NUMBER == 2:
        spider_thread1 = threading.Thread(target=start_list_spider_requests_fn, args=(spider_list_start_url,))
        spider_thread1.start()
        spider_thread2 = threading.Thread(target=start_list_spider_requests_fn, args=(spider_list_start_ur2,))
        spider_thread2.start()
    # spider_thread3 = threading.Thread(target=start_list_spider_requests_fn, args=(spider_list_start_ur3,))
    # spider_thread3.start()
    return HttpResponse("execute list spider successfully")


def list_page_process_fn(list_data):
    print('列表页数据插入')
    time_now = time.time()

    # 解压缩
    # decompress_data = zlib.decompress(list_data)
    # list_data = decompress_data.decode()

    data_loads = json.loads(list_data)

    print(type(data_loads))
    json_dict = json.loads(data_loads)

    bulk_insert_data = list()
    for item_data in json_dict["data"]:
        json_dict_houses = item_data['listings']
        bulk_insert_data += [RealtorListPageJson(json_data=json.dumps(house)) for house in json_dict_houses]
    print("list table 插入成功，批量插入了{}条".format(len(bulk_insert_data)))
    RealtorListPageJson.objects.bulk_create(bulk_insert_data)
    print("list 表跟新花费时间{}s".format(time.time() - time_now))


# 列表页数据的插入操作
def process_list_page_json(request):
    row_data = request.body
    executor.submit(list_page_process_fn,list_data=row_data)
    return HttpResponse("服务器已经接受到了list json  存储处理请求")


# 列表页抓取完全之后的数据处理操作
def spider_close_process(request):
    SpiderCloseProcess.spider_finish_flag += 1
    if SpiderCloseProcess.spider_finish_flag == SpiderCloseProcess.spider_client_count:
        print('list 客户端爬虫执行完成，处理数据并向客户端爬虫发送抓取数据url')
        close_spider_process = SpiderCloseProcess(PYMYSQL_POOL)
        close_spider_process.execute_spider_close()
        # SpiderCloseProcess.spider_finish_flag = 0
        return HttpResponseRedirect(redirect_post_detail_criteria_to_client_url)
        # return HttpResponse("还有客户端爬虫没有执行完全")
    return HttpResponse("还有客户端爬虫没有执行完全")




# def get_detail_search_criteria_fn():
#     get_detail_url = GetDetailSearchCriteria()
#     get_detail_url.get_detail_url()


def post_detail_criteria_to_client(request):
    PostDetailSearchCriteriaToClient.get_detail_url()
    return HttpResponse("detail 搜索条件发送到爬虫客户端成功")


def detail_spider_close_process(request):

    return HttpResponse("detail 爬虫执行完毕")






# def start_detial_spider_requests_fn(url):
#     requests.get(url=url)
#
#
# # 详情页爬虫启动
# def start_detail_spider(request):
#     print("启动详情页爬虫")
#     spider_thread1 = threading.Thread(target=start_detial_spider_requests_fn, args=(spider_detail_start_url,))
#     spider_thread1.start()
#     # spider_thread2 = threading.Thread(target=start_detial_spider_requests_fn, args=(spider_detail_start_url2,))
#     # spider_thread2.start()
#     # spider_thread3 = threading.Thread(target=start_detial_spider_requests_fn, args=(spider_detail_start_url3,))
#     # spider_thread3.start()
#     return HttpResponse("execute successfully")


def detail_json_process(detail_data):
    print("详情页数据插入")
    time_now = time.time()

    # decompress_data = zlib.decompress(detail_data)
    # detail_data = decompress_data.decode()

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


def json_data_get_test(request):
    return HttpResponse(
        "test successful!!!!"
    )


def post_json_data_test(request):
    data = request.get_body
    print(len(data))
    return HttpResponse("测试未压缩文件成功")


def post_compress_data_test(request):
    data = request.get_body
    print(len(data))
    return HttpResponse("测试压缩文件成功")







