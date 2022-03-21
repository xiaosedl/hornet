from ninja import Router, File
from ninja.files import UploadedFile

from backend.common import response, Error
from projects.api_schema import ProjectIn
from projects.models import Project

router = Router()


@router.post('/projects')
def get_project(request, payload: ProjectIn):
    """
    查询 projects
    """

    projects = "abc"  # 查询项目

    if projects:
        projects_info = []

        return response(result=projects_info)
    else:
        return response(error=Error.PROJECTS_IS_NULL)


@router.post('/create/', auth=None)
def create_project(request, payload: ProjectIn):
    """
    创建项目
    """

    name = payload.name
    describe = payload.describe
    image = payload.image

    project = Project.objects.filter(name=name)
    if len(project) > 0:
        return response(error=Error.PROJECT_ANME_EXIST)

    Project.objects.create(**payload.dict())
    return response()


@router.post('/upload/', auth=None)
def img_upload(request, file: UploadedFile = File(...)):
    """
    图片上传，接收 buye
    """
    data = file.read()
    return {"name": file.name, "len": len(data)}