from ninja import Router
from ninja import Schema
from django.contrib.auth.models import User

from backend.common import response, Error


router = Router()


class RegisterIn(Schema):
    username: str
    password: str
    confirm_password: str


class RegisterOut(Schema):
    id: int
    username: str
    email: str


@router.post('/register')
def user_register(request, payload: RegisterIn):
    """
    用户注册
    """
    if payload.password != payload.confirm_password:
        return response(error=Error.USER_OR_PAWD_ERROR)

    try:
        User.objects.get_by_natural_key(payload.username)
    except User.DoesNotExist:
        pass
    else:
        return response(error=Error.USER_EXIST)

    user = User.objects.create_user(username=payload.username, password=payload.password)
    user_info = {
        "id": user.id,
        "username": user.username
    }
    return response(result=user_info)