from ninja import Schema


class ProjectIn(Schema):
    """创建项目入参"""
    name: str
    describe: str = None
    image: str = None


class ProjectOut(Schema):
    project_name: str
    project_desc: str
    project_status: str
    project_create_time: str
