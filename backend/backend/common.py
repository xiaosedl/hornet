
class Error:
    """
    定义错误码与错误信息
    """

    USER_OR_PAWD_NULL = {"10010": "用户名或密码为空"}
    USER_OR_PAWD_ERROR = {"10011": "用户名或密码错误"}
    PAWD_ERROR = {"10012": "两次密码不一致"}
    USER_EXIST = {"10013": "用户已存在"}
    USER_NOT_EXIST = {"10014": "用户不存在"}

    PROJECTS_IS_NULL = {"20010": "项目查询结果为空"}
    PROJECT_ANME_EXIST = {"20011": "项目名称已存在"}
    PROJECT_NOT_EXIST = {"20012": "项目不存在存在"}
    PROJECT_IS_DEELEE = {"20013": "项目已经被删除"}

    IMAGE_SIZE_ERROR = {"30010": "不支持大于 20M 的图片上传"}
    IMAGE_TYPE_ERROR = {"30011": "图片类型错误"}


def response(success: bool = True, error: dict = None, item=None) -> dict:
    """
    定义统一返回格式
    """

    if error is None:
        error_code = ""
        error_msg = ""
    else:
        success = False
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]

    if item is None:
        item = []

    resp_dict = {
        "success": success,
        "error": {
            "code": error_code,
            "msg": error_msg
        },
        "item": item
    }

    return resp_dict