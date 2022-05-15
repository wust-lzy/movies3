# 前天登录权限验证中间件
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from movie3 import settings
from apps.common.models import Constant


# 定义登录权限验证中间件
class LoginMiddleware(MiddlewareMixin):

    # 在执行具体的请求之前，进行验证
    def process_request(self, request):
        path = request.path  # 请求的url
        print("权限验证:%s" % path)
        # 设置不需要登录就能够访问的url
        noAuthPath = ",/,/login,/doLogin,/register,/doRegister,/logout" \
                     ",/item/detail,"
        # 后台和上传的资源不需要验证
        if path.startswith(settings.MEDIA_URL) or path.startswith("/admin/"):
            pass
        else:
            path = "," + path + ","
            if path not in noAuthPath:
                # 判断session中是否有登录用户数据
                if request.session.get(Constant.session_user_isLogin, None):
                    pass
                else:
                    return HttpResponseRedirect('/login')  # 返回登录页面

