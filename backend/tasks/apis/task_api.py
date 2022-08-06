import json
from itertools import chain
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from backend.common import response, model_to_dict, Error
from backend.pagination import CustomPagination
from projects.models import Project
from tasks.apis.api_schema import TaskIn, TaskOut, ProjectIn, TaskCaseListIn
from cases.models import TestCase
from tasks.models import TestTask, TaskCaseRelevance
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

    case = json.dumps(data.cases)
    case_list = [case["casesId"] for case in data.cases]
    case_list = list(chain(*case_list))
    TaskCaseRelevance.objects.create(task_id=task.id, case=case, cases_sequence=case_list)
    task_dict = model_to_dict(task)
    task_dict["cases"] = case

    return response(item=task_dict)


@router.get("/list/", auth=None, response=List[TaskOut])
@paginate(CustomPagination)
def task_list(request, filters: ProjectIn = Query(...), **kwargs):
    """
    查询任务列表
    auth=None，该接口不需要认证
    """

    return TestTask.objects.filter(project_id=filters.project_id, is_delete=False).all().order_by('-id')


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

    relevance = TaskCaseRelevance.objects.get(task_id=task.id)
    task_dict = model_to_dict(task)
    task_dict["cases"] = json.loads(relevance.case)

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
    relevance = get_object_or_404(TaskCaseRelevance, task_id=task_id)

    task.name = data.name
    task.describe = data.describe
    task.save()

    case_list = [case["casesId"] for case in data.cases]
    case_list = list(chain(*case_list))
    relevance.case = json.dumps(data.cases)
    relevance.cases_sequence = case_list
    relevance.save()

    task_dict = model_to_dict(task)
    task_dict["cases"] = data.cases

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


@router.get("/{task_id}/cases/", auth=None)
def task_case_list(request, task_id: int):
    """
    获取任务的用例
    auth=None，该接口不需要认证
    """

    task = get_object_or_404(TestTask, pk=task_id)

    if task.is_delete is True:
        return response(error=Error.TASK_IS_DEELEE)

    relevance = TaskCaseRelevance.objects.get(task_id=task.id)
    case_list = json.loads(relevance.cases_sequence)
    cases_info = [model_to_dict(TestCase.objects.get(id=case)) for case in case_list]

    return response(item=cases_info)


@router.put("/{task_id}/cases/", auth=None)
def update_task_case_list(request, task_id: int, data: TaskCaseListIn):
    """
    更新用例执行顺序
    auth=None，该接口不需要认证
    """

    relevance = get_object_or_404(TaskCaseRelevance, task_id=task_id)
    relevance.cases_sequence = json.dumps(data.case_list)
    relevance.save()
    print(data.case_list)
    print(task_id)

    return response(item=[])

