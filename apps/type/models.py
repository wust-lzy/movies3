from django.db import models


class Type(models.Model):
    typename = models.CharField(max_length=255, blank=False, null=False,verbose_name="项目类型名称")

    # 这个是在后台编辑项目的时候列表显示类型名称而不是整个对象
    def __str__(self):
        return self.typename

    class Meta:
        managed = False
        db_table = 'type'
        verbose_name_plural = "项目类型"
        verbose_name = "项目类型"

