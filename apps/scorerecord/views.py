# 前台评分视图模块
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from apps.common.models import Constant
from apps.item.models import Item
from apps.scorerecord.models import Scorerecord
from apps.user.models import User
from apps.util.util import Util


# 添加评分记录
def doScorerecord(request):
    post = request.POST
    score = post.get("score")
    itemid = post.get("itemid")
    scorerecord = Scorerecord()
    item = Item()
    item.id = itemid
    scorerecord.itemid = item
    user = User()
    user.id = request.session[Constant.session_user_id]
    scorerecord.userid = user
    scorerecord.score = score
    scorerecord.createtime = Util().getCurrentTime()
    scorerecord.save()
    data = {
        "success":1,  # 1：操作成功
        "url":"reload"  # 重新加载请求的页面
    }
    return JsonResponse(data)


# 评分列表
def list(request):
    page = request.POST.get("page",1)
    userid = request.session[Constant.session_user_id]
    scorerecords = Scorerecord.objects.filter(userid_id=userid).order_by("-id")
    paginator = Paginator(scorerecords, Constant.pageSize)
    scorerecords = paginator.page(page)
    data = {
        "pageBean":scorerecords,
        "page":page,
    }
    return render(request,"scorerecord/list.html",context=data)