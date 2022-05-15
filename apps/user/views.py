from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.common.models import Constant
from apps.user.models import User


# 跳转到用户编辑页面
def edit(request):
    user = User.objects.get(id=request.session[Constant.session_user_id])
    data = {
        "user": user,
    }
    return render(request, "user/edit.html", context=data)


# 保存用户修改的数据
def doEdit(request):
    post = request.POST
    email = post.get("email")
    success = User.objects.filter(id=request.session[Constant.session_user_id])\
        .update(email=email)
    data = {
        "success":success,
        "url":"reload",
    }
    return JsonResponse(data)





