from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from apps.common.models import Constant
from apps.user.models import User
from apps.util.util import Util


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'createtime']
    search_fields = ['username']
    list_per_page = Constant.pageSizeAdmin
    fields = ["username","email",'createtime']
    readonly_fields = ["username","email",'createtime']








