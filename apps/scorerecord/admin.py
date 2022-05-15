# 后台admin评分功能
from django.contrib import admin
from apps.common.models import Constant
from apps.scorerecord.models import Scorerecord
from apps.util.util import Util


# 后台admin的评分功能类
@admin.register(Scorerecord)  # 将scorerecord类加入后台admin管理
class ScorerecordAdmin(admin.ModelAdmin):
    # 列表展示字段
    list_display = ['showUsername', 'showItemname','score','createtime']
    # 列表展示字段添加链接（跳转到详情或者修改页面）
    list_display_links = ['showUsername', 'showItemname',]
    # 列表展示字段添加链接（跳转到详情或者修改页面）
    search_fields = ['userid__username','itemid__itemname']
    # 每页展示的条数
    list_per_page = Constant.pageSizeAdmin
    # 编辑页面需要编辑的字段
    fields = ["userid","itemid","score"]
    # 只读字段
    readonly_fields = ["userid","itemid","score"]
    # 列表页面的过滤器过滤字段
    list_filter = ('score',)

    # 列表展示页面，有些字段需要格式化或者显示外键的某些属性，用户外键的用户名
    def showUsername(self,obj):
        return obj.userid.username

    # 设置字段显示的标题
    showUsername.short_description = '用户名'

    # 列表展示页面，有些字段需要格式化或者显示外键的某些属性，项目外键的项目名
    def showItemname(self,obj):
        return obj.itemid.itemname

    # 设置字段显示的标题
    showItemname.short_description = '项目标题'


