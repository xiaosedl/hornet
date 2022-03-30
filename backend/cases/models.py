from django.db import models
from projects.models import Project


class Module(models.Model):
    """
    模块(节点)表
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=1000, null=False, default="")
    describe = models.CharField("描述", max_length=1000, null=True, blank=True, default="")
    parent_id = models.IntegerField("父级ID", default=0)
    is_delete = models.BooleanField("删除", default=False)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
