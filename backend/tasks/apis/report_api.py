from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from backend.common import response
from backend.pagination import CustomPagination
from cases.apis.api_schema import ProjectIn
from tasks.apis.api_schema import ResultOut
from tasks.models import TestResult, TestTask

router = Router()  # 实例化 project 的路由 Router


@router.get("/list/", auth=None, response=List[ResultOut])
@paginate(CustomPagination)
def report_list(request, filters: ProjectIn = Query(...), **kwargs):
    """
    查询报告列表
    auth=None，该接口不需要认证
    """

    tasks = TestTask.objects.filter(project_id=filters.project_id, is_delete=False).all()
    task_ids = [task.id for task in tasks]
    return TestResult.objects.filter(task_id__in=task_ids).all().order_by('-id')


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