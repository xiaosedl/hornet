from ninja import Schema


class RegisterIn(Schema):
    """注册用户入参"""
    username: str
    password: str
    confirm_password: str


class RegisterOut(Schema):
    """注册用户出参"""
    id: int
    username: str
    email: str


class LoginIn(Schema):
    """用户登录入参"""
    username: str
    password: str