import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
dot_env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dot_env_path):
    load_dotenv(dot_env_path)
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_KEY = os.getenv("JWT_KEY")
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "Application.Supply.apps.ApplicationConfig",
    "Application.Database.apps.DatabaseConfig",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "Components.Middlewares.auth.AuthMiddleware",
]

ROOT_URLCONF = "DjangoConfig.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "DjangoConfig.wsgi.application"

database_name = os.getenv("NAME")
database_user = os.getenv("USER")
database_password = os.getenv("PASSWORD")
database_host = os.getenv("HOST")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": database_name,
        "USER": database_user,
        "PASSWORD": database_password,
        "HOST": database_host,
        "PORT": 3306,
    }
}

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
LOCATION = os.getenv("LOCATION")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": LOCATION,  # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 1000, "encoding": "utf-8"},
            # "PASSWORD": "qwe123"  # redis密码
        },
    }
}

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = False

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 配置匿名用户
REST_FRAMEWORK = {"UNAUTHENTICATED_USER": None, "UNAUTHENTICATED_TOKEN": None}

# 媒体文件目录
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# 媒体文件url
MEDIA_URL = "/media/"
# 文件上传的路径
UPLOAD_PATH = "upload/"

# 百度文字识别API


ocr_id = os.getenv("BAIDU_API_ID")
ocr_api_key = os.getenv("BAIDU_API_KEY")
ocr_secret_key = os.getenv("BAIDU_SECRET_KEY")
