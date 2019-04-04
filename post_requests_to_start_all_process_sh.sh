#!/bin/bash

project1='post_request_to_start_all_process.py'


for Pro in $project1

do

PythonPid=`ps -ef | grep $Pro | grep -v grep | wc -l `

echo $Pro
if [ $PythonPid -eq 0 ];
        then
        echo "`date "+%Y-%m-%d %H:%M:%S"`:$Pro is not running" >> /usr/project/AmericaSpiderDjangoServer/realtor_server.log

        cd /usr/project/AmericaSpiderDjangoServer

        nohup python $Pro  > post_requests_start_all_process.out 2>&1 &

        echo "`date "+%Y-%m-%d %H:%M:%S"`:$Pro is starting" >> /usr/project/AmericaSpiderDjangoServer/realtor_server.log
        sleep 5
        CurrentPythonPid=`ps -ef | grep $Pro | grep -v grep | wc -l`
        if [ $CurrentPythonPid -ne 0 ];
        then
        echo "`date "+%Y-%m-%d %H:%M:%S"`:$Pro is running" >> /usr/project/AmericaSpiderDjangoServer/realtor_server.log
        fi
fi
done