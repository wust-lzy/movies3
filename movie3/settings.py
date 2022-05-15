# 在setting.py中定义全局变量，该变量的变量名需要全部大写，否则会引用不到
import os
from pathlib import Path

# 项目根目录：F:\pycharmworkspace\WebMovieCFRSPython
BASE_DIR = Path(__file__).resolve().parent.parent

# setting中的加密盐,该配置是django的安全配置，防止攻击用的，该值是startProject时用系统的某个算法产生的.
SECRET_KEY = 'ncskr#$o88fj7@tprzvr2f0g98z^kcqtr+y9h2o)a%5*7b^fyw'

# 调试模式是否开启
DEBUG = True

# 访问web服务的的Ip配置,用于配置能够访问当前站点的域名（IP地址），
# 当 DEBUG = False 时，必须填写，有以下三种使用方法：
# []，空列表,表示只有127.0.0.1，localhost能访问本项目；
# ['*']，表示任何网络地址都能访问到当前项目；
# ['192.168.1.3', '192.168.3.3'] 表示只有当前两个主机能访问当前项目。
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'movie3.colaplusice.com']

# app应用的安装配置
INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.index.apps.AppsConfig',  # 自定义app,前台首页
    'apps.user.apps.AppsConfig',  # 自定义app,用户
    'apps.type.apps.AppsConfig',  # 自定义app,项目类型
    'apps.item.apps.AppsConfig',  # 自定义app,项目
    'apps.scorerecord.apps.AppsConfig',  # 自定义app,评分记录
    'apps.common.apps.AppsConfig'  # 自定义app,公共
]

# django的中间件配置，即MIDDLEWARE设置，
# 所谓中间件就是从用户请求到用户请求结束期间所做的操作，
# 即用户的请求会次从上到下依次执行MIDDLEWARE中的配置，
# 然后服务器响应用户的时候会再次从下至上依次执行，
# 在request请求前后，和response响应前后执行
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 安全中间件
    'django.contrib.sessions.middleware.SessionMiddleware',  # 会话中间件， 启用会话框架
    'django.middleware.common.CommonMiddleware',  # 通用中间件
    # CSRF防御中间件,增加防御保护以防止跨站伪造请攻击。通过向表单Post请求中添加隐藏表单字段以及对请求进行检查以获取正确的值。
    'django.middleware.csrf.CsrfViewMiddleware',
    # admin用户认证中间件,在每个HttpRequest请求对象中添加user属性，表名当前已登录的用户
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 消息中间件，提供Django的cookie以及session框架的支持，这两个基于消息中间件实现。
    'django.contrib.messages.middleware.MessageMiddleware',
    # X框架操作中间件，通过头部信息中增加X-Frame-OptionsLAI 防止简单的点击劫持。
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 前台登录权限验证中间件，自定义
    'apps.common.loginMiddleware.LoginMiddleware',
]

# 指定根级url的配置
ROOT_URLCONF = 'movie3.urls'

# 它用于指定模板的配置信息，列表中每一元素都是一个字典。如下所示是 Django 默认自带模板引擎
# 全局上下文处理器提供的变量优先级高于单个视图函数给单个模板传递的变量。
# 这意味着全局上下文处理器提供的变量可能会覆盖你视图函数中自定义的本地变量，
# 因此请注意避免本地变量名与全局上下文处理器提供的变量名称重复。
# 这些变量名包括perms, user和debug等等。
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # 默认使用的模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 模板路径
        'APP_DIRS': True,  # 引擎是否在已安装应用程序（的目录）内查找模板源文件。
        'OPTIONS': {  # 传递给模板引擎的其他参数
            'context_processors': [  # 上下文处理器，也可以自定义，这样就可以在模板中直接使用debug、request、auth、message变量
                # 在模板里面可以直接使用settings的DEBUG参数以及强大的sql_queries:它本身是一个字典，
                # 其中包括当前页面执行SQL查询所需的时间
                'django.template.context_processors.debug',
                # 在模板中可以直接使用request对象
                'django.template.context_processors.request',
                # 在模板里面可以直接使用user，perms对象。
                'django.contrib.auth.context_processors.auth',
                # 在模板里面可以直接使用message对象。
                'django.contrib.messages.context_processors.messages',
                # 也可以继续添加
                # "django.template.context_processors.i18n",  # 在模板里面可以直接使用settings的LANGUAGES和LANGUAGE_CODE
                # 'django.template.context_processors.media',  # 可以在模板里面使用settings的MEDIA_URL参数
                # 'django.template.loaders.filesystem.Loader',
                # 'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

# 项目部署时，Django的内置服务器将使用的WSGI应用程序对象的完整Python路径。
WSGI_APPLICATION = 'movie3.wsgi.application'

# 数据库链接配置，也可以已配置文件的形式加载数据库信息，django目前支持sqlite、mysql、postgreSQL、oracle数据库
# sqlite数据库：'django.db.backends.sqlite3',
#  postgreSQL数据库：'django.db.backends.postgresql_psycopg2',
#  mysql数据库：'django.db.backends.mysql'
#  oracle数据库：'django.db.backends.oracle'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# 切换为mysql  删掉sqlite3 创建movie3数据库，运行sql文件
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'movie3',
#         'USER': 'root',
#         'PASSWORD': 'newpass',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }

# 这是一个支持插拔的密码验证器，且可以一次性配置多个，
# Django 通过这些内置组件来避免用户设置的密码等级不足的问题。
AUTH_PASSWORD_VALIDATORS = [
    {  # 检查密码和用户某些属性的相似性
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {  # 检查密码的最小长度(默认8)
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {  # 检查密码是否出现在常用密码表中
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {  # 检查密码是否全为数字
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 设置语言zh-hans，zh-cn，en-us
LANGUAGE_CODE = 'zh-hans'
# 设置时区Asia/Shanghai，UTC
TIME_ZONE = 'Asia/Shanghai'
# 设置国际化，根据个人需要进行设置：
USE_I18N = True
# 相同内容被不同时区地区的用户访问时，是否以不同格式内容展示(例如时间，日期，数字)
USE_L10N = True
# 设置保存到数据库时间类型是否为UTC时间，如果不需要请设置为false,默认为true
USE_TZ = True


# 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}
# 它指的是静态资源的存放位置，静态资源包括 CSS、JS、Images。比如我们要在项目中添加一些图片，
# 通常这些静态图片被存放在新建的 static 目录下，这样就实现了通过 STATIC_URL= '/static/' 路径对静态资源的访问。

static = os.path.dirname(os.path.abspath(__file__))
static = os.path.join(static, "../")
STATICFILES_DIRS = (os.path.join(static, "static"),)
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
# 线上设置
ENV_PROFILE = os.getenv("ENV")
# cdn url # collect static后，文件会在这里 方便在远程部署同步文件到nginx
if ENV_PROFILE == 'production':
    # cdn地址
    STATIC_URL = "http://static.colaplusice.com/movie3/static/"
    # nginx配置的文件目录
    STATIC_ROOT = "/www/movie3/static"
#
# 第三方配置
GRAVATAR_DEFAULT_URL = "http://www.example.com/mydefaultavatar.jpg"
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
