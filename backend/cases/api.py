from django.forms import model_to_dict
from ninja import Router

from cases.api_schema import ModuleIn
from backend.common import Error, response
from cases.models import Module
from projects.models import Project

router = Router()


@router.post('/', auth=None)
def create_module(request, payload: ModuleIn):
    """
    创建模块
    auth=None 该接口不需要认证
    """

    # 先检查选择项目是否存在
    project = Project.objects.filter(id=payload.project_id)
    if len(project) == 0:
        return response(error=Error.PROJECT_NOT_EXIST)

    module = Module.objects.filter(name=payload.name, project_id=payload.project_id)
    if len(module) > 0:
        return response(error=Error.MODULE_NAME_EXIST)

    module = Module.objects.create(**payload.dict())
    return response(item=model_to_dict(module))
