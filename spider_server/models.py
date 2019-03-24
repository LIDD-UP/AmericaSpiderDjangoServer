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
    json_data = models.TextField(null=True)
    last_operation_date = models.DateTimeField('操作时间', default=timezone.now,null=True)

    class Meta:
        db_table = 'tb_realtor_list_page_json'


class RealtorListPageJsonSplite(models.Model):
    property_id = models.BigIntegerField(primary_key=True)
    last_update = models.TextField(null=True)
    address = models.TextField(null=True)
    last_operation_date = models.DateTimeField('操作时间', default=timezone.now,null=True)
    lat = models.TextField(null=True)
    lon = models.TextField(null=True)
    beds = models.TextField(null=True)
    sqft = models.TextField(null=True)
    baths = models.TextField(null=True)
    price = models.TextField(null=True)
    lot_size = models.TextField(null=True)

    class Meta:
        db_table = 'tb_realtor_list_page_json_splite'


class RealtorDetailJson(models.Model):
    property_id = models.BigIntegerField(primary_key=True)
    last_update = models.TextField(null=True)
    address = models.TextField(null=True)
    last_operation_date = models.DateTimeField('操作时间', default=timezone.now,null=True)
    lat = models.TextField(null=True)
    lon = models.TextField(null=True)
    beds = models.TextField(null=True)
    sqft = models.TextField(null=True)
    baths = models.TextField(null=True)
    price = models.TextField(null=True)
    lot_size = models.TextField(null=True)
    data_interface = models.TextField(null=True)
    is_dirty = models.TextField(null=True)
    detail_json = models.TextField(null=True)

    class Meta:
        db_table = 'tb_realtor_detail_json'







