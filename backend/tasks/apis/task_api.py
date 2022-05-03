from typing import List

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from backend.common import response, model_to_dict, Error
from backend.pagination import CustomPagination
from cases.models import TestCase
from projects.models import Project
from tasks.apis.api_schema import TaskIn, ResultOut
from tasks.models import TestTask, TaskCaseRelevance, TestResult
from tasks.task_running.task_runner import thread_run

router = Router()  # 实例化 project 的路由 Router


@router.post("/", auth=None)
def task_create(request, data: TaskIn):
    """
    创建任务
    auth=None，该接口不需要认证
    """

    project = get_object_or_404(Project, pk=data.project)
    task = TestTask.objects.create(project_id=project.id, name=data.name, describe=data.describe)
    cases = []
    for case in data.cases:
        TaskCaseRelevance.objects.create(task_id=task.id, case_id=case)
        case = TestCase.objects.get(pk=case)
        cases.append({
            "case": case.id,
            "module": case.module_id})
    task_dict = model_to_dict(task)
    task_dict["cases"] = cases

    return response(item=task_dict)


@router.get("/list/{task_id}/", auth=None, response=List[ResultOut])
@paginate(CustomPagination)
def task_list(request, task_id: int, **kwargs):
    """
    查询任务列表
    auth=None，该接口不需要认证
    """

    task = get_object_or_404(TestTask, pk=task_id)

    return TestResult.objects.filter(task=task).all()


@router.post("/{task_id}/running/", auth=None)
def task_running(request, task_id: int):
    """
    运行任务
    auth=None，该接口不需要认证
    """

    task = get_object_or_404(TestTask, pk=task_id)
    task.status = 1
    task.save()

    # 执行任务
    thread_run(task.id)

    return response()


@router.get("/{task_id}/", auth=None)
def task_detail(request, task_id: int):
    """
    任务详情
    auth=None，该接口不需要认证
    """

    task = get_object_or_404(TestTask, pk=task_id)

    if task.is_delete is True:
        return response(error=Error.TASK_IS_DEELEE)

    relevance = TaskCaseRelevance.objects.filter(task_id=task.id)
    cases_list = [rel.id for rel in relevance]
    task_dict = model_to_dict(task)
    task_dict["cases"] = cases_list

    return response(item=task_dict)


@router.put("/update/{task_id}/", auth=None)
def task_update(request, task_id: int, data: TaskIn):
    """
    更新任务:
    1. 获取原关联数据
    2. 删除原关联数据
    3. 新增需要更新的数据
    auth=None，该接口不需要认证
    """

    get_object_or_404(Project, pk=data.project)
    task = get_object_or_404(TestTask, pk=task_id)
    relvance = get_object_or_404(TaskCaseRelevance, task_id=task_id)

    cases = []
    for case in data.cases:
        try:
            TaskCaseRelevance.objects.create(task_id=task.id, case_id=case)
        except IntegrityError:
            return response(error=Error.CASE_NOT_EXIST)
        case = TestCase.objects.get(pk=case)
        cases.append({
            "case": case.id,
            "module": case.module_id})

    task.name = data.name
    task.describe = data.describe
    task.save()
    relvance.delete()
    task_dict = model_to_dict(task)
    task_dict["cases"] = cases

    return response(item=task_dict)


@router.delete("/delete/{task_id}/", auth=None)
def task_delete(request, task_id: int):
    """
    删除任务，逻辑删除
    auth=None，该接口不需要认证
    """

    task = get_object_or_404(TestTask, pk=task_id)
    task.is_delete = True
    task.save()

    return response()




