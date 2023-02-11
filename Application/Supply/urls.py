from django.urls import path
from rest_framework import routers

from .views import account, basic

router = routers.SimpleRouter()  # 实例化路由
router.register(r"basic", basic.BasicView)  # 注册路由
urlpatterns = [
    path("login/", basic.PwdLoginView.as_view()),
    path("send/sms/", basic.SendSmsView.as_view()),
    path("login/sms/", basic.SmsLoginView.as_view()),
    path("register/sms/", basic.RegisterSmsView.as_view()),
    path("register/", basic.RegisterView.as_view()),
]
urlpatterns += router.urls
