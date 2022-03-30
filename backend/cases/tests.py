from django.test import TestCase

import requests

for p in range(2):
    data = {
        "name": "三级模块" + str(p),
        "project_id": 1,
        "parent_id": 5
    }
    r = requests.post('http://127.0.0.1:8000/api/cases/', json=data)
    print(r.json())
