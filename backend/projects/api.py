import hashlib
import os
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, File
from ninja.files import UploadedFile
from ninja.pagination import paginate

from backend.common import response, Error
from backend.pagination import CustomPagination
from backend.settings import IMAGE_DIR
from projects.api_schema import CreateProjectIn, ProjectOut
from projects.models import Project

router = Router()  # 实例化 project 的路由 Router


@router.get('/list/', auth=None, response=List[ProjectOut])
@paginate(CustomPagination, page_size=6)  # type: ignore
def project_list(request, **kwargs):
    """
    获取项目列表
    auth=None 该接口不需要认证
    """

    return Project.objects.filter(is_delete=False).all()  # 查询 project 数据


@router.post('/', auth=None)
def project_create(request, payload: CreateProjectIn):
    """
    创建项目
    """

    project = Project.objects.filter(name=payload.name)
    if len(project) > 0:
        return response(error=Error.PROJECT_NAME_EXIST)

    Project.objects.create(**payload.dict())
    return response()


@router.get('/{project_id}/', auth=None)
def project_detail(request, project_id):
    """
    获取项目详情
    auth=None，该接口不需要认证
    """

    project = get_object_or_404(Project, id=project_id)  # django 的获取对象方法，没有返回 404 和 msg，节省捕捉异常逻辑
    if project.is_delete is True:
        return response(error=Error.PROJECT_IS_DEELEE)

    data = {
        "id": project.id,
        "name": project.name,
        "describe": project.describe,
        "image": project.image,
        "create_time": project.create_time
    }
    return response(item=data)


@router.put('/update/{project_id}/', auth=None)
def project_update(request, project_id: int, payload: CreateProjectIn):
    """
    更新项目信息
    """

    project = get_object_or_404(Project, id=project_id)
    for attr, value in payload.dict().items():
        setattr(project, attr, value)  # 更新对象数据简便方法
    project.save()
    return response()


@router.delete('/delete/{project_id}/', auth=None)
def project_update(request, project_id: int):
    """
    删除项目信息
    """

    project = get_object_or_404(Project, id=project_id)
    project.is_delete = True
    project.save()
    return response()


@router.post('/upload', auth=None)
def project_img_upload(request, file: UploadedFile = File(...)):
    """
    项目图片上传
    1. post 方法 + form-data 格式
    2. 名称，大小
    3. 上传的文件需要保存：读取上传文件内容，写入到一个新文件中
    """

    # 获取上传文件后缀
    suffix = file.name.split(".")[-1]
    if suffix not in ["png", "jpg", "jpeg", "gif"]:
        return response(error=Error.IMAGE_TYPE_ERROR)

    # 图片大小 1024 * 1024 * 20 M
    if file.size > 20971520:
        return response(error=Error.IMAGE_SIZE_ERROR)

    # 文件名生成 md5
    file_md5 = hashlib.md5(bytes(file.name, encoding="utf8")).hexdigest()
    file_name = file_md5 + "." + suffix

    # 保存图片
    upload_file = os.path.join(IMAGE_DIR, file_name )
    with open(upload_file, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    return response(item=file_name)