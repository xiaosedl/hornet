from typing import Any
from datetime import datetime

from ninja import Schema


class TaskIn(Schema):
    """任务入参"""

    name: str
    project: int
    describe: str = None
    cases: list


class ResultOut(Schema):
    """任务出参"""

    name: str
    passed: int
    error: int
    failure: int
    skipped: int
    tests: int
    runtime: float
    create_time: datetime