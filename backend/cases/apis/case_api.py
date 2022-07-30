import json

import requests
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Router
import jmespath

from backend.common import Error, response
from cases.apis.api_schema import CaseIn, CaseDebugIn, CaseAssertIn, ExtractIn
from cases.models import Module, TestCase, TestExtract
from .common import get_replace_string

router = Router()


@router.post("/", auth=None)
def case_create(request, data: CaseIn):
    """
    创建用例
    auth=None，该接口不需要认证
    """

    data_ = data.dict()
    resp = json.loads(data.response)
    extract_list = data_.pop("extract_list")
    module = get_object_or_404(Module, id=data.module_id)

    case_obj = TestCase.objects.filter(name=data.name)
    if case_obj.exists():
        return response(error=Error.CASE_NAME_EXIST)
    case = TestCase.objects.create(**data_)

    for extract in extract_list:
        if extract["name"] == "" or extract["extract"] == "":
            continue
        result = jmespath.search(extract["extract"], resp)
        extract_obj = TestExtract.objects.filter(project_id=module.project_id, name=extract["name"])
        if len(extract_obj) > 0:
            extract_obj.extract = extract["extract"]
        else:
            TestExtract.objects.create(
                project_id=module.project_id,
                case_id=case.id,
                name=extract["name"],
                extract=extract["extract"],
                value=result
            )

    return response(item=model_to_dict(case))


@router.post('/debug/', auth=None)
def case_debug(request, data: CaseDebugIn):
    """
    测试用例调试
    auth=None，该接口不需要认证
    """

    method = data.method.value
    params_type = data.params_type.value
    url = get_replace_string(data.url)
    headers = {key: get_replace_string(value) for key, value in data.header.items()}
    body = {key: get_replace_string(value) for key, value in data.params_body.items()}

    if method == "GET" and params_type.title() == "Params":
        resp = requests.request(method=method, url=url, headers=headers, params=body).text
    elif method in ["POST", "PUT", "DELETE"] and params_type.title() == "Form":
        resp = requests.request(method=method, url=url, headers=headers, data=body).text
    elif method in ["POST", "PUT", "DELETE"] and params_type.title() == "Json":
        resp = requests.request(method=method, url=url, headers=headers, json=body).text
    else:
        return response(error=Error.CASE_REQUEST_ERROR)

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
    else:
        return response()


@router.put("/update/{case_id}", auth=None)
def case_update(request, case_id: int, data: CaseIn):
    """
    用例更新
    auth=None，该接口不需要认证
    """

    data_ = data.dict()
    resp = json.loads(data.response)
    extract_list = data_.pop("extract_list")
    module = get_object_or_404(Module, id=data.module_id)
    case = get_object_or_404(TestCase, id=case_id)

    for attr, value in data_.items():
        setattr(case, attr, value)
    case.save()

    for extract in extract_list:
        if extract["name"] == "" or extract["extract"] == "":
            continue
        result = jmespath.search(extract["extract"], resp)
        extract_obj = TestExtract.objects.filter(project_id=module.project_id, name=extract["name"])
        if extract_obj.exists() and extract_obj[0].case_id != case.id:
            Error.CASE_EXTRACT_ERROR["10056"] = f"提取器 {extract_obj[0].name} 已存在，id：{extract_obj[0].case_id}"
            return response(error=Error.CASE_EXTRACT_ERROR)
        elif extract_obj.exists() and extract_obj[0].case_id == case.id:
            extract_obj.update(extract=extract["extract"], value=result)
        else:
            TestExtract.objects.create(
                project_id=module.project_id,
                case_id=case.id,
                name=extract["name"],
                extract=extract["extract"],
                value=result
            )

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

    case = get_object_or_404(TestCase, id=case_id)
    if case.is_delete is True:
        return response(error=Error.CASE_IS_DELETE)
    extract_obj = TestExtract.objects.filter(case_id=case_id)
    extract_list = []
    for extract in extract_obj:
        extract_list.append(
            {"name": extract.name,
             "extract": extract.extract}
        )
    case_ = model_to_dict(case)
    case_["extract_list"] = extract_list

    return response(item=case_)


@router.post('/extract', auth=None)
def check_extract(request, data: ExtractIn):
    """
    检查用例提取器
    auth=None，该接口不需要认证
    """

    resp = json.loads(data.response)
    extract_list = data.extract_list
    module = get_object_or_404(Module, id=data.module_id)

    for extract in extract_list:
        extract_obj = TestExtract.objects.filter(project_id=module.project_id, name=extract["name"])
        if extract_obj.exists() and extract_obj[0].case_id != data.case_id:
            Error.CASE_EXTRACT_ERROR["10056"] = f"提取器 {extract_obj[0].name} 已存在，id：{extract_obj[0].case_id}"
            return response(error=Error.CASE_EXTRACT_ERROR)
        extract_name = extract["name"]
        extract_value = extract["extract"]
        if extract_name == '' or extract_value == '':
            continue
        result = jmespath.search(extract_value, resp)
        if result is None:
            Error.CASE_EXTRACT_ERROR["10056"] = f"提取器错误：{extract_value}"
            return response(error=Error.CASE_EXTRACT_ERROR)

    return response()
