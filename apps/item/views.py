# 前台项目视图模块
from django.shortcuts import render

from apps.common.models import Constant
from apps.item.models import Item
from apps.scorerecord.models import Scorerecord


# 项目详情
def detail(request):
    # 通过get请求获取项目id，是其他页面跳转到项目详情页面
    # 通过post请求获取项目id，是在项目详情页面中的评分请求中获取
    itemid = request.GET.get("itemid", request.POST.get("itemid"))
    # 查找当前项目
    item = Item.objects.get(id=itemid)
    data = {  # 返回参数
        "item": item,
    }
    # 判断游客是否登录
    if Constant.session_user_isLogin in request.session \
            and request.session[Constant.session_user_isLogin]:
        userid = request.session[Constant.session_user_id]
        # 获取登录用户是否对当前项目评分
        scorerecord = Scorerecord.objects.filter(userid_id=userid, itemid_id=itemid)
        if len(scorerecord) > 0:
            data["scorerecord"] = scorerecord[0]
    return render(request, "item/detail.html", context=data)
