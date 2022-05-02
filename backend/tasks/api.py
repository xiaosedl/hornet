import json
import os

from django.shortcuts import get_object_or_404
from ninja import Router

from backend.common import response, model_to_dict
from backend.settings import BASE_DIR
from cases.models import TestCase
from projects.models import Project
from tasks.api_schema import TaskIn
from tasks.models import TestTask, TaskCaseRelevance
from tasks.task_running.test_result import save_test_result

router = Router()  # 实例化 project 的路由 Router


TEST_DATA = os.path.join(BASE_DIR, "tasks", "task_running", "test_data.json")
TEST_CASE = os.path.join(BASE_DIR, "tasks", "task_running", "test_case.py")


@router.post("/", auth=None)
def create_task(request, data: TaskIn):
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


@router.post("/{task_id}/running/", auth=None)
def running_task(request, task_id: int):
    """
    运行任务
    auth=None，该接口不需要认证
    """

    task = get_object_or_404(TestTask, pk=task_id)
    relevance = TaskCaseRelevance.objects.filter(task_id=task.id)

    test_cases = {}
    for rel in relevance:
        try:
            case = TestCase.objects.get(pk=rel.case_id, is_delete=False)
            header_dict = json.loads(case.header)
            params_body = case.params_body.replace("\'", "\"")
            params_body_dict = json.loads(params_body)
            test_cases[case.name] = {
                "url": case.url,
                "method": case.method,
                "header": header_dict,
                "params_type": case.params_type,
                "params_body": params_body_dict,
                "assert_type": case.assert_type,
                "assert_body": case.assert_text
            }
        except TestCase.DoesNotExist:
            pass

    with open(TEST_DATA, 'w') as fj:
        fj.write(json.dumps(test_cases))
    os.system(f"python3 {TEST_CASE}")

    save_test_result(task_id)

    return response()