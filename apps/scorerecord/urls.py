"""
前台评分功能url
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from apps.scorerecord import views

urlpatterns = [
    path('doScorerecord',views.doScorerecord),  # 添加评分记录
    path('list',views.list),  # 评分记录列表
]
