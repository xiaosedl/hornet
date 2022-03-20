from ninja import Router, Schema

from backend.common import response, Error

router = Router()


class GetProjectIn(Schema):
    project_id: str = None
    project_status: int = None
    project_name: str
    page: int = 1
    limit: int = 10


class GetProjectOut(Schema):
    project_name: str
    project_desc: str
    project_status: str
    project_create_time: str


@router.post('/projects')
def get_project(request, payload: GetProjectIn):
    """
    查询 projects
    """

    projects = "abc"  # 查询项目

    if projects:
        projects_info = [
            {
                "project_name": payload.project_name,
                "project_desc": payload.project_id,
                "project_status": payload.project_status,
                "project_create_time": payload.limit
            },
            {
                "project_name": payload.project_name,
                "project_desc": payload.project_id,
                "project_status": payload.project_status,
                "project_create_time": payload.limit, }
        ]
        return response(result=projects_info)
    else:
        return response(error=Error.PROJECTS_IS_NULL)
