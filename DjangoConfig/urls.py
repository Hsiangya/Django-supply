from django.urls import path

from ApplicationSupply.views import (
    PwdLoginView,
    RegisterSmsView,
    RegisterView,
    SendSmsView,
    SmsLoginView,
)

urlpatterns = [
    path("api/login/password/", PwdLoginView.as_view()),
    path("api/send/sms/", SendSmsView.as_view()),  # 已注册的手机验证码API
    path("api/login/sms/", SmsLoginView.as_view()),
    path("api/register/", RegisterView.as_view()),
    path("api/register/sms/", RegisterSmsView.as_view()),  # 未注册的手机验证码API
]
