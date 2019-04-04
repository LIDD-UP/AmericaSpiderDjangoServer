#!/bin/bash
tmp=`ps -ef | grep "/usr/bin/python manage.py runserver 0.0.0.0:8000"| grep -v grep | awk '{print $2}'`
echo ${tmp}
kill -9 ${tmp}