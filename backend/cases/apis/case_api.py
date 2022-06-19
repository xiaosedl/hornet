import requests
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Router

from backend.common import Error, response
from cases.apis.api_schema import CaseIn, CaseDebugIn, CaseAssertIn
from cases.models import Module, TestCase

router = Router()


@router.post("/", auth=None)
def case_create(request, data: CaseIn):
    """
    创建用例
    auth=None，该接口不需要认证
    """

    case = Module.objects.filter(id=data.module_id)
    if len(case) == 0:
        return response(error=Error.MODULE_NOT_EXIST)
    case_exist = TestCase.objects.filter(name=data.name)
    if case_exist:
        return response(error=Error.CASE_NAME_EXIST)
    case = TestCase.objects.create(**data.dict())
    return response(item=model_to_dict(case))


@router.post('/debug/', auth=None)
def case_debug(request, data: CaseDebugIn):
    """
    测试用例调试
    auth=None，该接口不需要认证
    """

    method = data.method.value
    params_type = data.params_type.value

    if method == "GET" and params_type.title() == "Params":
        resp = requests.request(method=method, url=data.url, headers=data.header, params=data.params_body).text
    elif method in ["POST", "PUT", "DELETE"] and params_type.title() == "Form":
        resp = requests.request(method=method, url=data.url, headers=data.header, data=data.params_body).text
    elif method in ["POST", "PUT", "DELETE"] and params_type.title() == "Json":
        resp = requests.request(method=method, url=data.url, headers=data.header, json=data.params_body).text
    else:
        return response(error=Error.CASE_REQEUST_ERROR)
    return response(item={"response": resp})


@router.post("/assert/", auth=None)
def cast_assert(request, data: CaseAssertIn):
    """
    断言判断
    auth=None，该接口不需要认证
    """

    resp = data.response
    assert_type = data.assert_type.value
    assert_text = data.assert_text

    if assert_type == "include":
        if assert_text in resp:
            return response()
        else:
            return response(success=False)
    elif assert_type == "equal":
        if assert_text == resp:
            return response()
        else:
            return response(success=False)
    return response()


@router.put("/update/{case_id}", auth=None)
def case_update(request, case_id: int, data: CaseIn):
    """
    用例更新
    auth=None，该接口不需要认证
    """

    case = get_object_or_404(TestCase, id=case_id)
    for attr, value in data.dict().items():
        setattr(case, attr, value)
    case.save()
    return response()


@router.delete("/delete/{case_id}", auth=None)
def case_delete(request, case_id):
    """
    删除测试用例
    auth=None，该接口不需要认证
    """

    case = get_object_or_404(TestCase, id=case_id)
    case.is_delete = True
    case.save()
    return response()


@router.get('/{case_id}/', auth=None)
def case_detail(request, case_id):
    """
    获取用例详情
    auth=None，该接口不需要认证
    """

    case = get_object_or_404(TestCase, id=case_id)  # django 的获取对象方法，没有返回 404 和 msg，节省捕捉异常逻辑
    if case.is_delete is True:
        return response(error=Error.CASE_IS_DEELEE)
    return response(item=case)