import os
from pathlib import Path
from xml.dom.minidom import parse
from tasks.models import TestResult


BASIC_DIR = Path(__file__).resolve().parent
TEST_REPORT = os.path.join(BASIC_DIR, "xml_test_report.xml")


def save_test_result(task_id):
    """
    保存测试结果
    """

    # 获取 xml dom 树
    dom = parse(TEST_REPORT)

    # 获取 xml 所有元素
    root = dom.documentElement

    # 获取 testsuite 节点
    testsuite = root.getElementsByTagName("testsuite")

    # 获取 testsuite 各属性值
    name = testsuite[0].getAttribute("name")
    tests = testsuite[0].getAttribute("tests")
    time = testsuite[0].getAttribute("time")
    failures = testsuite[0].getAttribute("failures")
    errors = testsuite[0].getAttribute("errors")
    skipped = testsuite[0].getAttribute("skipped")
    passed = int(tests) - int(failures) - int(errors) - int(skipped)

    # 读取测试报告，并入库
    with open(TEST_REPORT, 'r') as f:
        result = f.read()

    TestResult.objects.create(
        task_id=task_id,
        name=name,
        passed=passed,
        error=errors,
        failure=failures,
        skipped=skipped,
        tests=tests,
        runtime=time,
        result=result
    )
