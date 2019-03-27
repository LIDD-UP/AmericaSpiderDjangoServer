# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: urls.py
@time: 2019/3/23
"""
from django.urls import path

from spider_server import views

urlpatterns = [
    path('index/', views.index, name='index'),
    # # 开启列表页爬虫之前的数据库操作
    path('process_before_start_list_spider/', views.process_before_start_list_spider, name='process_before_start_list_spider'),
    # 开启列表页爬虫
    path('start_list_spider/', views.start_list_spider, name='start_list_spider'),
    # 列表页数据的插入操作
    path('process_list_page_json/', views.process_list_page_json, name='process_list_page_json'),
    # 列表页抓取完全之后的数据处理操作
    path('spider_close_process/', views.spider_close_process, name='spider_close_process'),
    # 详情页爬虫启动
    # path('start_detail_spider/', views.start_detail_spider, name='start_detail_spider'),
    # 详情页数据插入
    path('process_detail_page_json/', views.process_detail_page_json, name='process_detail_page_json'),
    # 异步测试
    path('json_data_get_test/',views.json_data_get_test, name='json_data_get_test'),
    path('post_detail_criteria_to_client/',views.post_detail_criteria_to_client, name='post_detail_criteria_to_client'),
    path('post_json_data_test/', views.post_json_data_test, name='post_json_data_test'),
    path('post_compress_data_test/', views.post_compress_data_test, name='post_compress_data_test'),

]

