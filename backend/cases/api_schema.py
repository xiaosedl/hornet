from ninja import Schema


class ModuleIn(Schema):
    """模块入参"""

    name: str
    project_id: int
    parent_id: int = 0


class ProjectIn(Schema):
    """模块所属项目入参"""

    project_id: int
