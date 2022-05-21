from ninja import Schema
from typing import Any


class CreateProjectIn(Schema):
    """创建项目入参"""
    name: str
    describe: str = ""
    image: str = ""


class ProjectOut(Schema):
    """查询项目出参"""
    id: int
    name: str
    describe: str
    image: str
    create_time: Any
