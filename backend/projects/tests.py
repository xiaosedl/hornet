from django.test import TestCase

import requests

for p in range(10):
    data = {
        "name": f"测试系统{p}",
        "describe": f"测试系统{p}项目描述",
        "image": "alksjlkslkfj23xldfkj.png"
    }
    r = requests.post('http://127.0.0.1:8000/api/projects/create/', json=data)
    print(r)