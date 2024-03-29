"""
Django settings for wybj_drf project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-3=g-s9&s1xgta$-=&9=68*z0dqe6q=lnfy@)6ob5oumqk%w@5j"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.user",
    "apps.score",
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    # 下面这个app用于刷新refresh_token后，将旧的加到blacklist时使用
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "wybj_drf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wybj_drf.wsgi.application"

# 替换系统原本的用户model
AUTH_USER_MODEL = "user.UserProfile"

# 自定义用户认证
AUTHENTICATION_BACKENDS = (
    # 自定义认证的类的路径
    "apps.user.views.CustomBackend",
)

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",  # 使用mysql数据库
#         "NAME": "wybj_drf",  # 要连接的数据库
#         "USER": "root",  # 链接数据库的用于名
#         "PASSWORD": "123456",  # 链接数据库的用于名
#         # "HOST": "10.165.27.210",  # mysql服务监听的ip
#         "HOST": "192.168.12.7",
#         "PORT": 3306,  # mysql服务监听的端口
#         "ATOMIC_REQUEST": True,  # 设置为True代表同一个http请求所对应的所有sql都放在一个事务中执行
#         # (要么所有都成功，要么所有都失败)，这是全局性的配置，如果要对某个
#         # http请求放水（然后自定义事务），可以用non_atomic_requests修饰器
#         "OPTIONS": {
#             "init_command": "SET storage_engine=INNODB",  # 设置创建表的存储引擎为INNODB
#         },
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 配置restframework 的验证类
REST_FRAMEWORK = {
    # 配置restframework的权限验证为
    "DEFAULT_PERMISSION_CLASSES": (
        # 认证用户可读可写
        "rest_framework.permissions.IsAuthenticated",
        # 认证用户可读可写，非认证用户则只能GET,HEAD,OPTIONS。
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 增加simplejwt认证方式
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    # 配置默认全局分页
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

# simple JWT配置
SIMPLE_JWT = {
    # "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),  # Access Token的有效期
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),  # Access Token的有效期
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Refresh Token的有效期
}

# 手机验证的正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

# 邮箱验证的正则表达式
REGEX_EMAIL = (
    "^[a-z0-9A-Z]+[- | a-z0-9A-Z . _]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,}$"
)

# 云片网API
APIKEY = "73966ba57a4453fadcce63a230dc4150"


# 邮箱验证码
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.qq.com"
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "phchen0769@foxmail.com"
EMAIL_HOST_PASSWORD = "sdykrpblxozebfcd"  # 授权码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
