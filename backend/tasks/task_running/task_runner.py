import json
import os
import threading

from backend.settings import BASE_DIR
from cases.models import TestCase
from tasks.models import TaskCaseRelevance, TestTask
from tasks.task_running.test_result import save_test_result

TEST_DATA = os.path.join(BASE_DIR, "tasks", "task_running", "test_data.json")
TEST_CASE = os.path.join(BASE_DIR, "tasks", "task_running", "test_case.py")


def task_runner(task_id):
    """
    任务运行器
    """

    print("1. 读取任务的测试用例")
    relevance = TaskCaseRelevance.objects.filter(task_id=task_id)

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

    print("2. 将测试用例数据写到 test_data.json")
    with open(TEST_DATA, 'w') as fj:
        fj.write(json.dumps(test_cases))

    print("3. 命令行执行 test_case.py 文件运行用例")
    os.system(f"python3 {TEST_CASE}")

    print("4. 保存测试执行结果")
    save_test_result(task_id)

    print("5. 执行完成...")
    task = TestTask.objects.get(pk=task_id)
    task.status = 2
    task.save()


def run(task_id):
    """
    线程执行
    """

    threads = []
    t = threading.Thread(target=task_runner, args=(task_id,))
    threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()


def thread_run(task_id):
    """
    线程执行
    """

    threads = []
    t = threading.Thread(target=run, args=(task_id,))
    threads.append(t)

    for t in threads:
        t.start()

