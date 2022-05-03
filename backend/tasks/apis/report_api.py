from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from backend.common import response
from tasks.apis.api_schema import ResultOut
from tasks.models import TestResult

router = Router()  # 实例化 project 的路由 Router


@router.get("/{report_id}/", auth=None, response=List[ResultOut])
def report_detail(request, report_id: int):
    """
    获取测试报告详情
    auth=None 该接口不需要认证
    """

    return TestResult.objects.filter(pk=report_id).all()


@router.delete("/delete/{report_id}/", auth=None)
def report_delete(request, report_id: int):
    """
    删除测试报告
    auth=None 该接口不需要认证
    """

    result = get_object_or_404(TestResult, pk=report_id)
    result.delete()

    return response()