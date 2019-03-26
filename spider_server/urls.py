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
    path('get_list_search_criteria/', views.get_list_search_criteria, name='get_list_search_criteria'),
    # 开启列表页爬虫
    path('start_list_spider/', views.start_list_spider, name='start_list_spider'),
    # 列表页数据的插入操作
    path('process_list_page_json/', views.process_list_page_json, name='process_list_page_json'),
    # 列表页抓取完全之后的数据处理操作
    path('spider_close_process/', views.spider_close_process, name='spider_close_process'),
    # 详情页爬虫启动
    path('get_detail_search_criteria/', views.get_detail_search_criteria, name='get_detail_search_criteria'),
    path('start_detail_spider/', views.start_detail_spider, name='start_detail_spider'),
    # 详情页数据插入
    path('process_detail_page_json/', views.process_detail_page_json, name='process_detail_page_json'),
    # 异步测试
    path('async_test/', views.async_test, name='async_test'),
    path('json_data_get_test/',views.json_data_get_test, name='json_data_get_test')

]

