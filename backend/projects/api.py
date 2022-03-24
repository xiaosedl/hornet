from typing import List

from ninja import Router, File
from ninja.files import UploadedFile
from ninja.pagination import paginate

from backend.common import response, Error
from backend.pagination import CustomPagination
from projects.api_schema import CreateProjectIn, ProjectOut
from projects.models import Project

router = Router()


@router.get('/list', auth=None, response=List[ProjectOut])
@paginate(CustomPagination, page_size=6)  # type: ignore
def project_list(request, **kwargs):
    """
    获取项目列表
    auth=None 该接口不需要认证
    """
    data = [
        {
            "id": p.id,
            "name": p.name,
            "describe": p.describe,
            "image": p.image,
            "create_time": p.create_time
        }
        for p in Project.objects.filter(is_delete=True).all()
    ]

    return Project.objects.filter(is_delete=False).all()


@router.post('/create', auth=None)
def project_create(request, payload: CreateProjectIn):
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


@router.post('/upload', auth=None)
def img_upload(request, file: UploadedFile = File(...)):
    """
    图片上传，接收 buye
    """
    data = file.read()
    return {"name": file.name, "len": len(data)}
