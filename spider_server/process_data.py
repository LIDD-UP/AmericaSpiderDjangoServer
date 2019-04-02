# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: process_data.py
@time: 2019/3/15
"""
import json
import redis
# from tools import get_sql_con
import redis

import time
from spider_server.models import RealtorDetailJson
from django.db.models import Q
from AmericaSpiderDjangoServer.settings import SPIDER_CLIENT_NUMBER,spider_client_get_detail_search_criteria_url, spider_client_get_detail_search_criteria_url2
import requests
import threading


class RealtorListPageMysqlsqlPipeline(object):

    def __init__(self, pool):
        # self.conn = get_sql_con.get_sql_con()
        self.conn = pool.connection()
        self.cursor = self.conn.cursor()
        self.sql = '''
            insert into tb_realtor_list_page_json(json_data,last_operation_date) values(%s,now())
        '''
        self.houses = []

    def json_process(self, item_data):
        json_dict_houses = item_data['listings']
        self.houses += [json.dumps(house) for house in json_dict_houses]

    def bulk_insert_to_mysql(self, bulkdata):
        print("插入长度", len(bulkdata))
        self.cursor.executemany(self.sql, bulkdata)
        print("执行插入完毕")
        self.conn.commit()
        del self.houses[:]

    def process_item(self, item):
        json_item = json.loads(item)
        for item_data in json_item["data"]:
            self.json_process(item_data)
        self.bulk_insert_to_mysql(self.houses)


class RealtordetailPageMysqlPipeline(object):

    def __init__(self,pool):
        self.conn = pool.connection()
        self.cursor = self.conn.cursor()
        self.sql = '''
              UPDATE tb_realtor_detail_json set detail_json=%s ,is_dirty='0',last_operation_date=now(),data_interface='1'
              WHERE property_id =%s
            '''
        self.detail_houses = []

    def traversal_json_data(self,json_data):
        json_data = json.loads(json_data)
        for format_data in json_data['data']:
            self.detail_houses.append((json.dumps(format_data['detailJson']),int(json.dumps(format_data['propertyId']))))

        self.cursor.executemany(self.sql, self.detail_houses)
        print("插入数据成功")
        self.conn.commit()
        del self.detail_houses[:]


class RealtorListProcess(object):
    def __init__(self, pool):
        self.conn = pool.connection()

    def truncate_list_json_and_split_table(self):
        """
        清空realtor_list_page_json 表和realtor_list_page_json_split 表
        :return:
        """
        truncate_realtor_list_str = '''
            TRUNCATE tb_realtor_list_page_json;
        '''

        truncate_realtor_list_splite_str = '''
            TRUNCATE tb_realtor_list_page_json_splite
        '''
        cursor = self.conn.cursor()
        cursor.execute(truncate_realtor_list_str)
        cursor.execute(truncate_realtor_list_splite_str)
        self.conn.commit()
        self.conn.close()
        print('清空realtor_list_page_json 表和清空清空realtor_list_page_json_splite 表成功')


class SpiderCloseProcess(object):
    spider_client_count = SPIDER_CLIENT_NUMBER
    spider_finish_flag = 0

    def __init__(self, pool):
        self.conn = pool.connection()

    def update_detail_data(self, conn, batch_size):
        print("更新detail数据")
        cursor1 = conn.cursor()
        cursor2 = conn.cursor()
        realtor_update_property_id_sql_str = '''
            SELECT
                rl.property_id,
                rl.address,
                rl.lat,
                rl.lon,
                rl.beds,
                rl.sqft,
                rl.baths,
                rl.price,
                rl.lot_size 
            FROM
                tb_realtor_list_page_json_splite rl
                INNER JOIN tb_realtor_detail_json rd ON rl.property_id = rd.property_id 
            WHERE
            rl.address != rd.address 
            OR rl.address != rd.address
            OR rl.lat != rd.lat
            OR rl.lon != rd.lon
            OR rl.beds != rd.beds
            OR rl.sqft != rd.sqft
            OR rl.baths != rd.baths
            OR rl.price != rd.price
            OR rl.lot_size != rd.lot_size
        '''

        # 获取需要更新的数据
        results1 = cursor1.execute(realtor_update_property_id_sql_str)

        # 批量更新数据
        sql_string1 = '''
            UPDATE tb_realtor_detail_json rj 
            SET is_dirty = '1',
            rj.address = %s,
            last_operation_date = now(),
            rj.lat = %s,
            rj.lon = %s,
            rj.beds = %s,
            rj.sqft = %s,
            rj.baths = %s,
            rj.price = %s,
            rj.lot_size = %s
            WHERE
                rj.property_id =%s
        '''

        print('更新跟新了{}'.format(cursor1.rowcount))

        sql_string_list = []
        update_data_number = cursor1.rowcount
        update_count_number = 0
        update_count = int(update_data_number / batch_size)
        remainder_update_rows = update_data_number % batch_size

        for i in cursor1.fetchall():
            if update_count_number == update_count and remainder_update_rows != 0:
                # print(i)
                # print([i[1], i[2], [3], [4], [5], [6], [7], [8], i[0]])
                sql_string_list.append([i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[0]])
                if len(sql_string_list) == remainder_update_rows:
                    cursor2.executemany(sql_string1, sql_string_list)
                    sql_string_list = []

            if update_count_number < update_count:
                # print(i)
                # print(i)
                # print([i[1], i[2], [3], [4], [5], [6], [7], [8], i[0]])
                sql_string_list.append([i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[0]])
                if len(sql_string_list) == batch_size:
                    cursor2.executemany(sql_string1, sql_string_list)
                    update_count_number += 1
                    sql_string_list = []
        conn.commit()

    def splite_list_data(self, conn):
        print("拆分数据")
        cursor = conn.cursor()
        sql_string_splite = '''
            INSERT INTO tb_realtor_list_page_json_splite ( property_id, address, last_operation_date, lat, lon, beds, sqft, baths, price, lot_size ) SELECT
            rj.property_id,
            JSON_EXTRACT( rj.json_data, '$.address' ) AS address,
            now( ) AS last_operation_date,
            JSON_EXTRACT( rj.json_data, '$.lat' ) AS lat,
            JSON_EXTRACT( rj.json_data, '$.lon' ) AS lon,
            JSON_EXTRACT( rj.json_data, '$.beds' ) AS beds,
            JSON_EXTRACT( rj.json_data, '$.sqft' ) AS sqft,
            JSON_EXTRACT( rj.json_data, '$.baths' ) AS baths,
            JSON_EXTRACT( rj.json_data, '$.price' ) AS price,
            JSON_EXTRACT( rj.json_data, '$.lot_size' ) AS lot_size 
            FROM
                tb_realtor_list_page_json rj 
            WHERE
                rj.property_id IS NOT NULL 
            GROUP BY
                rj.property_id
        '''
        cursor.execute(sql_string_splite)
        print("拆分了{}条数据".format(cursor.rowcount))
        conn.commit()

    def insert_detail_data(self, conn):
        print('插入detail没有的property_id')
        cursor = conn.cursor()
        sql_string_insert = '''
            INSERT INTO tb_realtor_detail_json ( property_id,address,is_dirty, last_operation_date,lat, lon,beds,sqft,baths,price,lot_size) (
                SELECT
                    rl.property_id ,
                    rl.address ,
                    0,
                    now(),
                    rl.lat,
                    rl.lon,
                    rl.beds,
                    rl.sqft,
                    rl.baths,
                    rl.price,
                    rl.lot_size
                FROM
                    tb_realtor_list_page_json_splite rl
                    LEFT JOIN tb_realtor_detail_json rd ON rl.property_id = rd.property_id 
                WHERE
                    rd.property_id IS NULL
                )
        '''
        cursor.execute(sql_string_insert)
        print("插入detail 表没有的数据：{}条".format(cursor.rowcount))
        conn.commit()

    def delete_not_exit(self, conn, batch_size):
        print("删除split没有，但是detial有的数据数据")
        cursor1 = conn.cursor()
        cursor2 = conn.cursor()
        realtor_update_property_id_sql_str = '''
            SELECT
                rl.property_id
            FROM
                tb_realtor_detail_json rl
                LEFT JOIN tb_realtor_list_page_json_splite rd ON rl.property_id = rd.property_id 
            WHERE
                rd.property_id IS NULL
        '''

        # 获取需要更新的数据
        results1 = cursor1.execute(realtor_update_property_id_sql_str)

        # 批量更新数据
        sql_string1 = '''
            DELETE FROM tb_realtor_detail_json 
            WHERE property_id =%s
        '''

        print('数据删除个数{}'.format(cursor1.rowcount))

        sql_string_list = []
        update_data_number = cursor1.rowcount
        update_count_number = 0
        update_count = int(update_data_number / batch_size)
        remainder_update_rows = update_data_number % batch_size

        for i in cursor1.fetchall():
            if update_count_number == update_count and remainder_update_rows != 0:
                # print(i)

                sql_string_list.append([i[0]])
                if len(sql_string_list) == remainder_update_rows:
                    cursor2.executemany(sql_string1, sql_string_list)
                    sql_string_list = []

            if update_count_number < update_count:
                # print(i)
                # print(i)
                sql_string_list.append([i[0]])
                if len(sql_string_list) == batch_size:
                    cursor2.executemany(sql_string1, sql_string_list)

                    update_count_number += 1
                    sql_string_list = []
        conn.commit()

    def post_detail_search_criteria_to_spider_client(self, conn):
        cursor = conn.cursor()
        sql_string = '''
            SELECT
                property_id
            FROM
                tb_realtor_detail_json 
            where detail_json is NULL 
            OR is_dirty='1'
        '''
        cursor.execute(sql_string)
        print("详情页需要抓取{},插入到redis里面".format(cursor.rowcount))
        import time
        time_now = time.time()
        # 这里还是要进行一定的批量操作，以免出错；

        row_count = cursor.rowcount
        print("详情页插入了{}条".format(row_count))
        batch_insert_size = 100000

        conn.commit()
        print("详情页搜索条件发送到client花费时间{}s".format(time.time()-time_now))

    def execute_spider_close(self):
        conn = self.conn
        # 将realtor_list_json表中的数据拆分开,并删除空的情况
        self.splite_list_data(conn)
        # 找到有的propertyId 并且lastUpate和address字段改变了的，这里应该使用批量更新
        self.update_detail_data(conn, 100)
        # 找到detail_page_json 表中没有的propertyId，并将它插入到该表中；
        self.insert_detail_data(conn)
        # 删除在split中没有，但是detail有的数据
        # self.delete_not_exit(conn, 100)
        conn.close()


class PostDetailSearchCriteriaToClient(object):
    spider_client_count = SPIDER_CLIENT_NUMBER

    def __init__(self, pool):
        self.conn = pool.connection()
        cursor = self.conn.cursor()
        sql_string = '''
                    SELECT
                        property_id
                    FROM
                        tb_realtor_detail_json 
                    where detail_json is NULL 
                    OR is_dirty='1'
                '''
        cursor.execute(sql_string)
        self.realtor_detail_json_query_result = cursor.fetchall()



    @classmethod
    def json_data_encapsulation(cls, property_id_list):
        client_one_data_dict = {"data": property_id_list}
        client_one_data_json = json.dumps(client_one_data_dict)
        return client_one_data_json

    @classmethod
    def post_data_spider_client(cls, url, json_data):
        requests.post(url=url, json=json_data)

    def get_detail_url(self):
        realtor_detail_json_query_result_len = len(self.realtor_detail_json_query_result)
        split_index = int(realtor_detail_json_query_result_len/PostDetailSearchCriteriaToClient.spider_client_count)

        if PostDetailSearchCriteriaToClient.spider_client_count == 1:
            print('detail 只有一个客户端爬虫')
            client_one_data = [result[0] for result in self.realtor_detail_json_query_result]
            client_one_data_json = PostDetailSearchCriteriaToClient.json_data_encapsulation(client_one_data)
            print('一只爬虫需要抓取的搜索数量{}'.format(len(client_one_data)))
            requests.post(url=spider_client_get_detail_search_criteria_url, json=client_one_data_json)
        if PostDetailSearchCriteriaToClient.spider_client_count == 2:
            print('detail两个客户端爬虫')
            client_one_data = [result[0] for result in self.realtor_detail_json_query_result[:split_index]]
            print('爬虫1 数据量{}条'.format(len(client_one_data)))
            client_one_data_json = PostDetailSearchCriteriaToClient.json_data_encapsulation(client_one_data)

            client_two_data = [result[0] for result in self.realtor_detail_json_query_result[split_index:]]
            client_two_data_json = PostDetailSearchCriteriaToClient.json_data_encapsulation(client_two_data)
            print('爬虫2 数据量{}条'.format(len(client_two_data)))

            spider_client_one_thread = threading.Thread(target=PostDetailSearchCriteriaToClient.post_data_spider_client,args=(spider_client_get_detail_search_criteria_url,client_one_data_json))
            spider_client_two_thread = threading.Thread(target=PostDetailSearchCriteriaToClient.post_data_spider_client,args=(spider_client_get_detail_search_criteria_url2,client_two_data_json))
            spider_client_one_thread.start()
            spider_client_two_thread.start()


# 会出现内存不足的情况
# class PostDetailSearchCriteriaToClient(object):
#     realtor_detail_json_query_result = RealtorDetailJson.objects.filter(Q(detail_json=None) | Q(is_dirty='1'))
#     spider_client_count = SPIDER_CLIENT_NUMBER
#
#     @classmethod
#     def json_data_encapsulation(cls, property_id_list):
#         client_one_data_dict = {"data": property_id_list}
#         client_one_data_json = json.dumps(client_one_data_dict)
#         return client_one_data_json
#
#     @classmethod
#     def post_data_spider_client(cls, url, json_data):
#         requests.post(url=url, json=json_data)
#
#     @classmethod
#     def get_detail_url(cls):
#         realtor_detail_json_query_result_len = len(cls.realtor_detail_json_query_result)
#         split_index = int(realtor_detail_json_query_result_len / cls.spider_client_count)
#
#         if cls.spider_client_count == 1:
#             print('detail 只有一个客户端爬虫')
#             client_one_data = [result.property_id for result in cls.realtor_detail_json_query_result]
#             client_one_data_json = cls.json_data_encapsulation(client_one_data)
#             print('一只爬虫需要抓取的搜索数量{}'.format(len(client_one_data)))
#             requests.post(url=spider_client_get_detail_search_criteria_url, json=client_one_data_json)
#         if cls.spider_client_count == 2:
#             print('detail两个客户端爬虫')
#             client_one_data = [result.property_id for result in cls.realtor_detail_json_query_result[:split_index]]
#             print('爬虫1 数据量{}条'.format(len(client_one_data)))
#             client_one_data_json = cls.json_data_encapsulation(client_one_data)
#
#             client_two_data = [result.property_id for result in cls.realtor_detail_json_query_result[split_index:]]
#             client_two_data_json = cls.json_data_encapsulation(client_two_data)
#             print('爬虫2 数据量{}条'.format(len(client_two_data)))
#
#             spider_client_one_thread = threading.Thread(target=cls.post_data_spider_client, args=(
#             spider_client_get_detail_search_criteria_url, client_one_data_json))
#             spider_client_two_thread = threading.Thread(target=cls.post_data_spider_client, args=(
#             spider_client_get_detail_search_criteria_url2, client_two_data_json))
#             spider_client_one_thread.start()
#             spider_client_two_thread.start()


if __name__ == "__main__":
    # realtor list page process
    # dict_data = '''{"data":[{"listings":[{"property_id":"5528101208","listing_id":"652373674","prop_type":"condo","last_update":"2019-03-14T11:32:02Z","rdc_web_url":"https://www.realtor.com/realestateandhomes-detail/8253-Highway-98-D200_Navarre_FL_32566_M55281-01208","prop_sub_type":"condo","is_turbo":false,"address":"8253 Highway 98 Unit D200, Navarre, 32566","prop_status":"for_sale","price_raw":220000,"sqft_raw":1146,"list_date":"2019-03-14T11:40:37Z","office_name":"Re/Max Gulf Properties","products":["co_broke","basic_opt_in","co_broke"],"is_showcase":false,"price":"$220,000","beds":2,"baths":3,"sqft":"1,146 sq ft","lot_size":"1,307 sq ft lot","photo":"https://ap.rdcpix.com/1756448895/05fb1701ebdb475d2fa6e46f4bec2305l-m0x.jpg","is_cobroker":true,"short_price":"$220K","baths_half":1,"baths_full":2,"photo_count":25,"lat":30.4272976,"lon":-86.88539,"is_new_listing":true,"has_leadform":true,"page_no":1,"rank":1,"list_tracking":"type|property|data|prop_id|5528101208|list_id|652373674|page|rank|list_branding|listing_agent|listing_office|property_status|product_code|advantage_code^1|1|0|1|35T|9HU|0^^$0|1|2|$3|4|5|6|7|F|8|G|9|$A|H|B|I]|C|J|D|K|E|L]]"},{"property_id":"6049007396","listing_id":"652370298","prop_type":"single_family","last_update":"2019-03-13T22:28:13Z","rdc_web_url":"https://www.realtor.com/realestateandhomes-detail/2027-Heritage-Park-Way_Navarre_FL_32566_M60490-07396","is_turbo":false,"address":"2027 Heritage Park Way in Heritage Park, Navarre, 32566","prop_status":"for_sale","price_raw":415000,"sqft_raw":2676,"list_date":"2019-03-14T03:35:52Z","office_name":"Keller Williams Realty Navarre","products":["co_broke","basic_opt_in","co_broke"],"is_showcase":false,"price":"$415,000","beds":4,"baths":3,"sqft":"2,676 sq ft","lot_size":"0.26 acres","photo":"https://ap.rdcpix.com/694472650/cf1c33ba89af42adfd4bdb401dc8ca24l-m0x.jpg","is_cobroker":true,"short_price":"$415K","baths_full":3,"photo_count":63,"lat":30.407241,"lon":-86.840354,"is_new_listing":true,"has_leadform":true,"page_no":1,"rank":2,"list_tracking":"type|property|data|prop_id|6049007396|list_id|652370298|page|rank|list_branding|listing_agent|listing_office|property_status|product_code|advantage_code^1|2|0|1|35T|9HU|0^^$0|1|2|$3|4|5|6|7|F|8|G|9|$A|H|B|I]|C|J|D|K|E|L]]"}]},{"listings":[{"property_id":"5528101208","listing_id":"652373674","prop_type":"condo","last_update":"2019-03-14T11:32:02Z","rdc_web_url":"https://www.realtor.com/realestateandhomes-detail/8253-Highway-98-D200_Navarre_FL_32566_M55281-01208","prop_sub_type":"condo","is_turbo":false,"address":"8253 Highway 98 Unit D200, Navarre, 32566","prop_status":"for_sale","price_raw":220000,"sqft_raw":1146,"list_date":"2019-03-14T11:40:37Z","office_name":"Re/Max Gulf Properties","products":["co_broke","basic_opt_in","co_broke"],"is_showcase":false,"price":"$220,000","beds":2,"baths":3,"sqft":"1,146 sq ft","lot_size":"1,307 sq ft lot","photo":"https://ap.rdcpix.com/1756448895/05fb1701ebdb475d2fa6e46f4bec2305l-m0x.jpg","is_cobroker":true,"short_price":"$220K","baths_half":1,"baths_full":2,"photo_count":25,"lat":30.4272976,"lon":-86.88539,"is_new_listing":true,"has_leadform":true,"page_no":1,"rank":1,"list_tracking":"type|property|data|prop_id|5528101208|list_id|652373674|page|rank|list_branding|listing_agent|listing_office|property_status|product_code|advantage_code^1|1|0|1|35T|9HU|0^^$0|1|2|$3|4|5|6|7|F|8|G|9|$A|H|B|I]|C|J|D|K|E|L]]"},{"property_id":"6049007396","listing_id":"652370298","prop_type":"single_family","last_update":"2019-03-13T22:28:13Z","rdc_web_url":"https://www.realtor.com/realestateandhomes-detail/2027-Heritage-Park-Way_Navarre_FL_32566_M60490-07396","is_turbo":false,"address":"2027 Heritage Park Way in Heritage Park, Navarre, 32566","prop_status":"for_sale","price_raw":415000,"sqft_raw":2676,"list_date":"2019-03-14T03:35:52Z","office_name":"Keller Williams Realty Navarre","products":["co_broke","basic_opt_in","co_broke"],"is_showcase":false,"price":"$415,000","beds":4,"baths":3,"sqft":"2,676 sq ft","lot_size":"0.26 acres","photo":"https://ap.rdcpix.com/694472650/cf1c33ba89af42adfd4bdb401dc8ca24l-m0x.jpg","is_cobroker":true,"short_price":"$415K","baths_full":3,"photo_count":63,"lat":30.407241,"lon":-86.840354,"is_new_listing":true,"has_leadform":true,"page_no":1,"rank":2,"list_tracking":"type|property|data|prop_id|6049007396|list_id|652370298|page|rank|list_branding|listing_agent|listing_office|property_status|product_code|advantage_code^1|2|0|1|35T|9HU|0^^$0|1|2|$3|4|5|6|7|F|8|G|9|$A|H|B|I]|C|J|D|K|E|L]]"}]}]}'''
    # realtor_test_dict = RealtorListPageMysqlsqlPipeline()
    # realtor_test_dict.process_item(dict_data)

    # realtor detail page process

    # realtor_detail_test = RealtordetailPageMysqlPipeline()
    # item_data = json.dumps({"data": [{"detailJson": '{"11":"123"}', "propertyId": 123445678},
    #                                  {"detailJson": '{"11":"123"}', "propertyId": 123445678}]})
    # realtor_detail_test.traversal_json_data(item_data)

    # process before start list spider
    pass



