#!/bin/bash

project1='manage.py'


for Pro in $project1

do

PythonPid=`ps -ef | grep $Pro | grep -v grep | wc -l `

echo $Pro
if [ $PythonPid -eq 0 ];
        then
        echo "`date "+%Y-%m-%d %H:%M:%S"`:$Pro is not running" >> /usr/project/logs/python.log

        cd /usr/project/AmericaSpiderDjangoServer
        
        nohup python $Pro runserver 0.0.0.0:8000 > nohup.out 2>&1 &

        echo "`date "+%Y-%m-%d %H:%M:%S"`:$Pro is starting" >> /usr/project/logs/python.log
        sleep 5
        CurrentPythonPid=`ps -ef | grep $Pro | grep -v grep | wc -l`
        if [ $CurrentPythonPid -ne 0 ];
        then
        echo "`date "+%Y-%m-%d %H:%M:%S"`:$Pro is running" >> /usr/project/logs/python.log
        fi
fi
done
