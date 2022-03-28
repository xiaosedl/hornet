from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from ninja import Router

from backend.common import response, Error
from users.api_schema import RegisterIn, LoginIn

router = Router()


@router.post('/register', auth=None)
def user_register(request, payload: RegisterIn):
    """
    用户注册
    1. 对注册对用户进行存在性校验
    2. 注册成功返回该注册用户信息
    """

    username = payload.username
    password = payload.password
    confirm_password = payload.confirm_password

    if password != confirm_password:
        return response(error=Error.USER_OR_PAWD_ERROR)

    try:
        User.objects.get_by_natural_key(payload.username)
    except User.DoesNotExist:
        pass
    else:
        return response(error=Error.USER_EXIST)

    user = User.objects.create_user(username=username, password=password)
    user_info = {
        "id": user.id,
        "username": user.username
    }
    return response(item=user_info)


@router.post('/login', auth=None)
def user_login(request, payload: LoginIn):
    """
    用户登录
    1. 对用户进行校验
    2. 登录成功返回对应用户信息
    """

    username = payload.username
    password = payload.password
    user = auth.authenticate(username=username, password=password)  # 使用 django 自带的认证模块
    if user is not None:
        auth.login(request, user)  # 向 django-session 表新增一条数据
        token = Session.objects.last()
        user_info = {
            "id": user.id,
            "username": user.username,
            "token": token.session_key
        }
        return response(item=user_info)
    else:
        return response(error=Error.USER_NOT_EXIST)
