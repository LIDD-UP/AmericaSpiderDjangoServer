import json
import os
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
# print(BASE_DIR)
# sys.path.append(BASE_DIR)
from spider_server.models import RealtorListPageJson



os.environ.setdefault('DJANGO_SETTING_MODULE', 'AmericaSpiderDjangoServer.settings')
django.setup()

RealtorListPageJson.objects.create(json_data='{"aa":"bb"}')