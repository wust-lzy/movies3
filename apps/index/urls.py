"""
前台首页url
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from apps.index import views

urlpatterns = [
    path('',views.index),  # 首页url
    path('recommend',views.recommend),  # 首页url
    path('search',views.search),  # 首页url
]
