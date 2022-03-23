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
        page: int = Field(1, gt=0)

    def __init__(self, page_size: int = settings.PAGINATION_PER_PAGE) -> None:
        self.page_size = page_size

    def paginate_queryset(self, items: QuerySet, request: HttpRequest, **params: DictStrAny):
        page: int = params["pagination"].page  # type: ignore
        offset = (page - 1) * self.page_size
        data = {
            "items": items[offset: offset + self.page_size],
            "page": page,
            "size": self.page_size,
            "total": len(items),
        }
        return response(result=data)

