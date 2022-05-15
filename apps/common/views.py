# 公共视图模块
from django.http import JsonResponse
from django.shortcuts import render, redirect

from apps.common.models import Constant
from apps.user.models import User
from apps.util.util import Util


# 跳转到登录页面
def login(request):
    return render(request, "common/login.html")


# 登录
def doLogin(request):
    post = request.POST
    username = post.get('username')
    password = post.get('password')
    users = User.objects.filter(username=username, password=password)  # 查询用户
    success = 0
    message = ""
    url = ""
    if len(users) != 0:
        success = 1
        sessionUser = users[0]  # 当前登录用户对象
        # 将登录信息保存到session中
        request.session[Constant.session_user_isLogin] = True
        request.session[Constant.session_user_id] = sessionUser.id
        request.session[Constant.session_user_username] = sessionUser.username
        # 登录成功跳转到首页
        url = "/"
    else:
        message = "用户名或者密码错误！"
    return JsonResponse({"success": success, "message": message, "url": url})


# 跳转到注册页面
def register(request):
    return render(request, "common/register.html")


# 注册
def doRegister(request):
    post = request.POST
    username = post.get('username')
    password = post.get('password')
    users = User.objects.filter(username=username)  # 查询用户名是否已经存在
    success = 0
    message = ""
    url = ""
    if len(users) != 0:
        success = -1
        message = "操作失败！用户名已存在！"
    else:
        user = User()
        user.username = username
        user.password = password
        user.createtime = Util().getCurrentTime()
        user.save()  # 保存注册的用户
        success = 1
        url = "/login"  # 跳转到用户登录页面
    return JsonResponse({"success": success, "message": message, "url": url})


# 注销
def logout(request):
    if not request.session.get(Constant.session_user_isLogin, None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    del request.session[Constant.session_user_isLogin]
    del request.session[Constant.session_user_id]
    del request.session[Constant.session_user_username]
    return redirect('/')
