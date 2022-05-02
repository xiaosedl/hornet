from ninja import Schema


class TaskIn(Schema):
    """任务入参"""

    name: str
    project: int
    describe: str = None
    cases: list