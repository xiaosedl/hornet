from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Router, Query

from backend.common import Error, response, children_node, node_tree
from cases.apis.api_schema import ModuleIn, ProjectIn
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


@router.get("/tree", auth=None)
def get_module_tree(request, filters: ProjectIn = Query(...)):
    """
    获取项目树：
    1. 遍历所有有效项目数据
    2. 递归获取当前节点的所有子节点
    auth=None 该接口不需要认证
    """

    modules = Module.objects.filter(project_id=filters.project_id, is_delete=False)
    data_node = []
    for m in modules:
        data_node.append({
            "id": m.id,
            "parent_id": m.parent_id,
            "label": m.name,
            "children": []
        })

    data = []
    for n in data_node:
        is_child = children_node(data_node, n)  # --> True/False

        # 如果没有子节点且父级节点为 0，添加为最外层，否则递归递进节点层级
        if not is_child and n["parent_id"] == 0:
            data.append(n)
        elif is_child and n["parent_id"] == 0:
            ret = node_tree(data_node, n)
            data.append(ret)

    return response(item=data)


@router.delete('/delete/{module_id}', auth=None)
def module_delete(request, module_id: int):
    """
    删除模块信息
    """

    module = get_object_or_404(Module, id=module_id)
    module.is_delete = True
    module.save()
    return response()