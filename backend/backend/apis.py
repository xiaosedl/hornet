"""
统一管理 ninja 类型的 API
1. 导入每个 django app 的路由管理文件 api，必需是 ninja 的 Router 类型对象
2. apps 新增一个 route 对象，apps.add_router(), 第一个参数为导入的 app 的路由第一路径，分组使用 tag
"""


from ninja import NinjaAPI

from users.api import router as users_router


apis = NinjaAPI()


apis.add_router('/users', users_router, tags=["Users"])


