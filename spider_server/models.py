from django.db import models

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


class RealtorListJson(models.Model):
    # name = fields.MedialNameField()
    # other= fields.JSONField()
    json_data = models.TextField()