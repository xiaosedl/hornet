from django.db.models import QuerySet
from ninja import Field, Schema
from ninja.pagination import PaginationBase
from ninja.types import DictStrAny


class CustomPagination(PaginationBase):
    """
    自定义分页器
    """
    class Input(Schema):
        """分页器的入参"""
        page: int = Field(1, gt=0)
        size: int = 6

    class Output(Schema):
        """分页器出参 0.17 后需要"""
        success: bool = True
        code: dict = {"code": "", "msg": ""}
        page: int
        size: int
        total: int

    def paginate_queryset(self, items: QuerySet, pagination: Input, **params: DictStrAny):
        """定义返回内容"""
        page = pagination.page
        size = pagination.size
        offset = (page - 1) * size
        data = {
            "items": items[offset: offset + size],  # items 关键字，不能修改（0.17）
            "size": size,  # 每夜条数
            "page": page,  # 第几页
            "total": len(items),  # 总条数
        }
        return data
