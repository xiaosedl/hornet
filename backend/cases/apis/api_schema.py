from typing import Any

from ninja import Schema
from enum import Enum


class ModuleIn(Schema):
    """模块入参"""

    name: str
    project_id: int
    parent_id: int = 0


class ProjectIn(Schema):
    """模块所属项目入参"""

    project_id: int


class Method(str, Enum):
    """请求方式：GET/POST/DELETE/PUT"""
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"


class ParamsType(str, Enum):
    """请求内容类型：param/form-data/json"""

    params = "Params"
    form_data = "Form"
    json = "Json"


class AssetType(str, Enum):
    """include/equal"""

    include = "include"
    equal = "equal"


class CaseIn(Schema):
    """用例入参"""

    module_id: int
    url: str
    name: str
    method: Method
    header: dict
    params_type: str
    params_body: dict
    response: str
    assert_type: str
    assert_text: str


class CaseDebugIn(Schema):
    """用例请求/调试入参"""

    url: str
    method: Method
    header: dict
    params_type: ParamsType
    params_body: dict


class CaseAssertIn(Schema):
    """断言入参"""

    response: str
    assert_type: AssetType
    assert_text: str


class ModuleSchema(Schema):
    """用例所属模块参数"""

    id: int
    name: str


class CaseOut(Schema):
    """用例出参"""
    id: int
    module_id: int
    url: str
    name: str
    method: str
    module: ModuleSchema = None
    create_time: Any
    update_time: Any