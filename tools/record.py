# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: record.py
@time: 2019/3/26
"""
'''
一共三种情况：
    一种是将搜索条件全部插入的情况：
        总的运行路线是这样的：
            1：通过请求process_before_start_list_spider
            
        
'''


'''
数据测试效果：
    list 数据插入：5个一发的情况是：45分钟：30万数据量；
    每个requests最多1000条数据，发送时间在0~ 30 秒不等；
    
    详情页：50个一发：发送到服务器时间14秒左右；
    15:20开始启动：到15：57：速度
    具体速度：2000 秒抓了1180条数据：还没达到本地的一个爬虫的速度；
    
    现在测试每次发送100条数据：
    
    
    
    需要手动修改的地方：
        1：list 爬虫 爬取完成的spider_close 函数的处理：需要修改时间：目的是因为，数据处理是异步的，如果不加上时间，可能服务器
            中的数据没有完全插入，就开始了list 数据的处理
        2：detail爬虫结束的spider_close 函数中(在middleware）中，用于关闭客户端服务和服务器服务；
                这里需要添加时间延迟，但是这里可添加，可不添加，可以直接在服务器中添加异步处理，在服务器中添加时间延迟，在服务其中的
                close_server_fn函数中；
        3：关于关闭server脚本不同的处理方式，两个环境不同，所以，需要不同的匹配语句来获取执行的进程id号，然后去关闭它；
        
        
        
    还差最后的定时脚本问题：
    一共有4个脚本：
        1：1个开启爬虫服务端服务
        2：两个开启，爬虫客户端服务
        3：一个发送requests请求，用户执行整个过程；
        
        关于时间上的分配：
            1：首先开启服务器端服务，然后再开启两个爬虫客户端服务，最后开启requests请求服务，
            requests请求服务一定要和前面的服务有一定的时间间隔，以免前面三个服务未开启；
            
            
几个脚本的位置：
1：美国服务：/bin/sh /usr/project/AmericaSpiderDjangoServer/start_estate_realtor_server.sh
2：爬虫服务1：/bin/sh /data/project/AmericaSpiderClientServer/start_estate_realtor_client.sh
3：爬虫服务2：/bin/sh /data/project/AmericaSpiderClientServer/start_estate_realtor_client.sh
4：requests请求：/bin/sh /usr/project/AmericaSpiderDjangoServer/post_requests_to_start_all_process_sh.sh
    
    

    
'''