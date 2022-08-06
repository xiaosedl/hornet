from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from backend.common import response
from backend.pagination import CustomPagination
from cases.apis.api_schema import ProjectIn, ExtractOut
from tasks.models import TestResult, TestTask
from cases.models import TestExtract
from backend.common import model_to_dict

router = Router()  # 实例化 project 的路由 Router


@router.get("/list/", auth=None, response=List[ExtractOut])
@paginate(CustomPagination)
def extract_list(request, filters: ProjectIn = Query(...), **kwargs):
    """
    查询报告列表
    auth=None，该接口不需要认证
    """

    return TestExtract.objects.filter(project_id=filters.project_id, is_delete=False).all()


@router.get("/{report_id}/", auth=None)
def report_detail(request, report_id: int):
    """
    获取测试报告详情
    auth=None 该接口不需要认证
    """

    result = get_object_or_404(TestResult, pk=report_id)
    return response(item=result)


@router.delete("/delete/{report_id}/", auth=None)
def report_delete(request, report_id: int):
    """
    删除测试报告
    auth=None 该接口不需要认证
    """

    result = get_object_or_404(TestResult, pk=report_id)
    result.delete()

    return response()
