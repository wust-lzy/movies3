# 前台首页视图模块
import operator
from math import sqrt

from django.core.paginator import Paginator
from django.shortcuts import render

from apps.common.models import Constant
from apps.item.models import Item
from apps.scorerecord.models import Scorerecord
from apps.type.models import Type


# 前台首页
def index(request):
    page = request.POST.get("page", 1)
    typeid = request.POST.get("typeid", "")  # 类型主键
    types = Type.objects.all()
    items = None
    if typeid == "":
        items = Item.objects.all().order_by("-id")  # 获取所有项目，id降序排列
    else:
        typeid = int(typeid)
        items = Item.objects.filter(typeid_id=typeid).order_by("-id")
    paginator = Paginator(items, Constant.pageSize)  # 分页
    items = paginator.page(page)
    data = {  # 返回参数
        "pageBean": items,
        "types": types,
        "typeid": typeid,
        "page": page,
    }
    return render(request, "index/index.html", context=data)


def search(request):
    page = request.POST.get("page", 1)
    typeid = request.POST.get("typeid", "")  # 类型主键
    types = Type.objects.all()
    if request.method == "POST":  # 如果搜索界面
        key = request.POST.get('keyword')
        if key :
            request.session["keyword"] = key  # 记录搜索关键词解决跳页问题
        else:
            key=request.session.get("keyword")
    else:
        key = request.session.get("keyword")  # 得到关键词
    items = Item.objects.filter(itemname__icontains=key)  # 进行内容的模糊搜索
    paginator = Paginator(items, Constant.pageSize)  # 分页
    items = paginator.page(page)
    data = {  # 返回参数
        "pageBean": items,
        "types": types,
        "typeid": typeid,
        "page": page,
    }
    return render(request, "index/index.html", context=data)


# 推荐项目（基于用户的协同过滤推荐算法）
def recommend(request):
    # 返回参数
    data = {}
    # 当前登录用户id
    currentUserid = request.session.get(Constant.session_user_id)
    currentUserid = int(currentUserid)
    # 获取所有评分数据
    scorerecords = Scorerecord.objects.all()

    data_dic = {}  # 创建一个空字典,保存用户-项目评分矩阵
    # 遍历评分数据
    for scorerecord in scorerecords:
        userid = scorerecord.userid_id  # 用户id
        itemid = scorerecord.itemid_id  # 项目id
        rating = int(scorerecord.score)  # 评分
        if not userid in data_dic.keys():
            data_dic[userid] = {itemid: rating}
        else:
            data_dic[userid][itemid] = rating

    if len(data_dic) == 0:
        print("没有评分数据！")
        return render(request, "index/recommend.html", context=data)

    if not currentUserid in data_dic.keys():
        print("目标用户没有评分！")
        return render(request, "index/recommend.html", context=data)

    # 计算用户相似度（余弦算法）
    similarity_dic = {}
    similarity_dic[currentUserid] = 0
    for userid, items in data_dic.items():  # 遍历所有用户
        if currentUserid != userid:  # 非目标用户
            # 余弦算法
            # 计算分子
            temp = 0
            temp2 = 0
            temp3 = 0
            for itemid, rating in data_dic[currentUserid].items():  # 遍历目标用户的评分项目
                if itemid in items.keys():  # 计算公共的项目的评分
                    # 注意，distance越大表示两者越相似
                    temp += float(rating) * float(items[itemid])
                    temp2 += pow(float(rating), 2)
                    temp3 += pow(float(items[itemid]), 2)
            distance = 0
            if temp2 == 0 or temp3 == 0:
                distance = 0
            else:
                distance = temp / (sqrt(temp2) * sqrt(temp3))
            similarity_dic[userid] = distance
            print("userid:" + str(currentUserid) + "    与userid：" + str(userid) + "    相似度=" + str(distance))
    print("用户相似度：")
    print(similarity_dic)
    # 排序，返回list类型
    similarity_dic = sorted(similarity_dic.items(), key=operator.itemgetter(1), reverse=True);  # 最相似的N个用户
    print("目标用户邻居：")
    print(similarity_dic)
    similarity_dic = similarity_dic[:10]  # 列表转字典
    similarity_dic = [(key, value) for key, value in similarity_dic if value > 0]
    print("目标用户最近邻居：%s" % similarity_dic)
    similarity_dic = dict(similarity_dic)

    # 推荐，预测评分
    # 先计算目标用户的平均评分
    sum_rating = 0
    for itemid, rating in data_dic[currentUserid].items():
        sum_rating += float(rating)
    # 目标用户对项目的平均评分
    avg_rating = sum_rating / len(data_dic[currentUserid].items())
    # 推荐
    item_rec_dic = {}
    # 遍历用户相似度
    for userid, similarity in similarity_dic.items():
        for itemid, rating in data_dic[userid].items():
            if not itemid in data_dic[currentUserid].keys():
                if not itemid in item_rec_dic.keys():
                    item_rec_dic[itemid] = {userid: rating}
                else:
                    item_rec_dic[itemid][userid] = rating
    print("所有推荐项目：")
    print(item_rec_dic)
    # 最终推荐的项目
    item_rec_final_dic = {}
    for itemid, item in item_rec_dic.items():
        if len(item) > 1:
            pre_score1 = 0
            pre_score2 = 0
            for userid, rating in item.items():
                pre_score1 += similarity_dic[userid] * (rating - avg_rating)
                pre_score2 += similarity_dic[userid]
            pre_score = avg_rating + pre_score1 / pre_score2
            # 预测评分
            item_rec_final_dic[itemid] = pre_score
    print("所有推荐项目和预测评分：")
    print(item_rec_final_dic)
    # 排序，根据预测评分
    item_rec_final_dic = sorted(item_rec_final_dic.items(), key=operator.itemgetter(1), reverse=True);
    print("最终推荐项目和预测评分：")
    item_rec_final_dic = item_rec_final_dic[:12]
    print(item_rec_final_dic)

    # 查找推荐结果
    if (item_rec_final_dic is not None) and (len(item_rec_final_dic) > 0):
        cfItemidsList = list()
        for cfItemid, pre in item_rec_final_dic:
            cfItemidsList.append(int(cfItemid))
        # 查询推荐的商品数据
        data["userCfItems"] = Item.objects.filter(id__in=cfItemidsList)

    return render(request, "index/recommend.html", context=data)
