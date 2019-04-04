import requests

req = requests.get(url='http://138.197.143.39:8000/spider_server/process_before_start_list_spider/')
print(req.status_code)
print('requests send successful')