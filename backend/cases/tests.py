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


# dict01 = {"name": "denlee", "age": 18}
# d = dict01.pop("name")
# print(d)
# print(dict01)

import re

s = '{"name": ${name}/abc, "age": ${age}, "sex": "M"}'
pattern = re.compile(r'\${' + r'\w+' + r'}', re.M | re.S)
ss = re.findall(pattern, str(s))
print("ss:", ss)
for v in ss:
    name = v.split('{')[1][:-1]
    print(v)
    print(name)
new_s = re.sub(pattern, "baidu", str(s))
print("new:", new_s)
