from django.test import TestCase

# import requests
#
# for p in range(2):
#     data = {
#         "name": "四级模块" + str(p),
#         "project_id": 1,
#         "parent_id": 8
#     }
#     r = requests.post('http://127.0.0.1:8000/api/cases/module/', json=data)
#     print(r.json())


dict01 = {"name": "denlee", "age": 18}
d = dict01.pop("name")
print(d)
print(dict01)
