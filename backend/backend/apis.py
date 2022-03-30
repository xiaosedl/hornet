"""
统一管理 ninja 类型的 API
1. 导入每个 django app 的路由管理文件 api，必需是 ninja 的 Router 类型对象
2. apps 新增一个 route 对象，apps.add_router(), 第一个参数为导入的 app 的路由第一路径，分组使用 tag
3. 定义全局接口认证，默认开启，若不通过，API 会自动获取异常并返回
"""

from django.contrib.sessions.models import Session
from ninja import NinjaAPI
from ninja.security import HttpBearer

from backend.settings import SESSION_COOKIE_AGE
from users.api import router as users_router
from projects.api import router as projects_router
from cases.api import router as cases_router


class InvalidToken(Exception):
    """无效 token"""
    pass


class ExpireToken(Exception):
    """过期 token"""
    pass


class GlobalAuth(HttpBearer):

    def authenticate(self, request, token):
        """
        自定义认证 token 处理
        """

        try:
            session = Session.objects.get(pk=token)
            # todo session 过期处理逻辑
        except Session.DoesNotExist:
            raise InvalidToken
        else:
            return token


apis = NinjaAPI(auth=GlobalAuth())


@apis.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    """
    无效 token 返回类型
    """

    return apis.create_response(request, {"detail": "Invalid token"}, status=401)


@apis.exception_handler(ExpireToken)
def on_expire_token(request, exc):
    """
    过期 token 返回类型
    """

    return apis.create_response(request, {"detail": "Expire token"}, status=401)


# tags users URI: api/users/xxx
apis.add_router('/users/', users_router, tags=["Users"])
# tags projects URI: api/projects/xxx
apis.add_router('/projects/', projects_router, tags=['Projects'])
# tags cases URI: api/cases/xxx
apis.add_router('/cases/', cases_router, tags=['Cases'])
