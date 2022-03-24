from typing import List, Any, Optional

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Field, Schema
from ninja.conf import settings
from ninja.pagination import PaginationBase
from ninja.types import DictStrAny

from backend.common import response


class CustomPagination(PaginationBase):
    """
    自定义分页器
    """
    class Input(Schema):
        """分页器的入参"""
        page: int = Field(1, gt=0)

    def __init__(self, page_size: int = settings.PAGINATION_PER_PAGE) -> None:
        self.page_size = page_size
        super().__init__()  # 执行 PaginationBase 本身的 __init__ 方法

    class Output(Schema):
        """分页器出参 0.17 后需要"""
        items: List[Any]
        page: int
        size: int
        total: int

    def paginate_queryset(self, items: QuerySet, pagination: Input, **params: DictStrAny):
        """定义返回内容"""
        page: int = pagination.page
        offset = (page - 1) * self.page_size
        data = {
            "items": items[offset: offset + self.page_size],
            "size": self.page_size,
            "page": page,
            "total": len(items),
        }
        return data
