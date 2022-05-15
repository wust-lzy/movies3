from django.contrib import admin
from apps.common.models import Constant
from apps.type.models import Type


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['typename']
    search_fields = ['typename']
    list_per_page = Constant.pageSizeAdmin
    fields = ["typename"]
