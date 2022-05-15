# 定义项目实体类
from django.db import models

from apps.util.util import Util


class Item(models.Model):
    itemname = models.CharField(max_length=255, blank=False, null=False, verbose_name="项目标题")
    # 项目类型外键，typeid其实是一个项目类型对象
    typeid = models.ForeignKey('type.Type', models.CASCADE,
                               db_column='typeid', blank=False, null=False, verbose_name="项目类型")
    # image = models.CharField(max_length=255, blank=True, null=True)
    # 图片字段
    image = models.ImageField(upload_to=Util().upload_path_handler, blank=False, null=False, verbose_name="封面")
    content = models.TextField(blank=False, null=False, verbose_name="项目简介", max_length=2000)
    createtime = models.CharField(max_length=255, blank=False, null=False, verbose_name="添加时间")

    # 这个是在后台编辑项目的时候列表显示对象属性值而不是整个对象
    def __str__(self):
        return self.itemname

    # 嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准
    class Meta:
        # 默认值为True,这个选项为True时Django可以对数据库表进行migrate或migrations、删除等操作
        # 如果为False的时候，不会对数据库表进行创建、删除等操作。可以用于现有表、数据库视图等，其他操作是一样的
        managed = False
        db_table = 'item'  # 对应的数据库表
        verbose_name_plural = "项目"  # 这个选项是指定，模型的复数形式是什么
        verbose_name = "项目"  # 给模型类起一个更可读的名字
