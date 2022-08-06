from typing import Any
from datetime import datetime

from ninja import Schema


class TaskIn(Schema):
    """任务入参"""

    name: str
    project: int
    describe: str = None
    cases: list


class TaskOut(Schema):
    """任务入参"""

    id: int
    name: str
    describe: str = None
    status: int
    update_time: Any


class ResultOut(Schema):
    """任务出参"""

    id: int
    name: str
    passed: int
    error: int
    failure: int
    skipped: int
    tests: int
    runtime: float
    result: str
    create_time: datetime


class ProjectIn(Schema):
    """任务所属项目入参"""

    project_id: int


class TaskCaseListIn(Schema):
    """更改用例顺序入参"""

    case_list: list
