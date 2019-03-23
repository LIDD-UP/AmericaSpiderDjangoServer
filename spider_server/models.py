from django.db import models
import django.utils.timezone as timezone

# Create your models here.
import json
# from django.contrib.postgres.fields import JSONField


# class JSONField(models.TextField):
#     # __metaclass__ = models.SubfieldBase
#     description = "Json"
#     def to_python(self, value):
#         v = models.TextField.to_python(self, value)
#         try:
#             return json.loads(v)['v']
#         except:
#             pass
#         return v
#     def get_prep_value(self, value):
#         return json.dumps({'v':value})


class RealtorListPageJson(models.Model):
    json_data = models.TextField()
    last_operation_date = models.DateTimeField('操作时间', default=timezone.now)

    class Meta:
        db_table = 'tb_realtor_list_page_json'


class RealtorListPageJsonSplite(models.Model):
    property_id = models.BigIntegerField(primary_key=True)
    last_update = models.DateTimeField('上次更新时间', default=timezone.now)
    address = models.TextField()
    last_operation_date = models.DateTimeField('操作时间', default=timezone.now)
    lat = models.TextField()
    lon = models.TextField()
    beds = models.TextField()
    sqft = models.TextField()
    baths = models.TextField()
    price = models.TextField()
    lot_size = models.TextField()

    class Meta:
        db_table = 'tb_realtor_list_page_json_splite'


class RealtorDetailJson(models.Model):
    property_id = models.BigIntegerField(primary_key=True)
    last_update = models.DateTimeField('上次更新时间', default=timezone.now)
    address = models.TextField()
    last_operation_date = models.DateTimeField('操作时间', default=timezone.now)
    lat = models.TextField()
    lon = models.TextField()
    beds = models.TextField()
    sqft = models.TextField()
    baths = models.TextField()
    price = models.TextField()
    lot_size = models.TextField()
    data_interface = models.TextField()
    is_dirty = models.TextField()
    detail_json = models.TextField()

    class Meta:
        db_table = 'tb_realtor_detail_json'





