from itertools import chain


class Error:
    """
    定义错误码与错误信息
    """

    USER_OR_PAWD_NULL = {"10010": "用户名或密码为空"}
    USER_OR_PAWD_ERROR = {"10011": "用户名或密码错误"}
    PAWD_ERROR = {"10012": "两次密码不一致"}
    USER_EXIST = {"10013": "用户已存在"}
    USER_NOT_EXIST = {"10014": "用户不存在"}

    PROJECTS_IS_NULL = {"10010": "项目查询结果为空"}
    PROJECT_NAME_EXIST = {"10021": "项目名称已存在"}
    PROJECT_NOT_EXIST = {"10022": "项目不存在存在"}
    PROJECT_IS_DEELEE = {"10023": "项目已经被删除"}

    IMAGE_SIZE_ERROR = {"10031": "不支持大于 20M 的图片上传"}
    IMAGE_TYPE_ERROR = {"10032": "图片类型错误"}

    MODULE_IS_NULL = {"10040": "模块查询结果为空"}
    MODULE_NAME_EXIST = {"10041": "模块名称已存在"}
    MODULE_NOT_EXIST = {"10042": "模块存在"}
    MODULE_IS_DEELEE = {"10043": "模块已经被删除"}

    CASE_IS_NULL = {"10050": "测试用例查询结果为空"}
    CASE_NAME_EXIST = {"10051": "测试用例名称已存在"}
    CASE_NOT_EXIST = {"10052": "测试用例存在"}
    CASE_IS_DEELEE = {"10053": "测试用例已经被删除"}
    CASE_REQEUST_ERROR = {"10054": "请求方法和类型不符：[GET]-[Param]，[POST/PUT]-[Form/Json]"}
    ASSERT_TYPE_ERROR = {"10055": "断言类型错误"}


def model_to_dict(instance: object) -> dict:
    """
    对象转字典
    """

    opts = instance._meta  # type: ignore
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    return data


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
    elif isinstance(item, dict):
        item = item
    elif isinstance(item, object):
        item = model_to_dict(item)

    resp_dict = {
        "success": success,
        "error": {
            "code": error_code,
            "msg": error_msg
        },
        "item": item
    }

    return resp_dict


def node_tree(nodes, current_node):
    """
    递归：获取 curent_node 的所有子节点
    """

    for node in nodes:
        if node["parent_id"] == current_node["id"]:
            current_node["children"].append(node)
            node_tree(nodes, node)  # 递归继续获取子节点，直到 nodes 遍历结束
    return current_node


def children_node(nodes, cureent_node):
    """
    判断当前有没有子节点
    """

    for node in nodes:
        if node["parent_id"] == cureent_node["id"]:
            return True
    return False