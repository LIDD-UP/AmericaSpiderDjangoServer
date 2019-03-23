# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: te_sql_insert.py
@time: 2019/3/23
"""

from spider_server.models import RealtorListJson

RealtorListJson.objects.create(name="C1", other=(1,2,3,4,5))