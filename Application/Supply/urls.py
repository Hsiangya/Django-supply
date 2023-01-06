from django.urls import path

from .views import account, basic

urlpatterns = [
    path("login/", basic.PwdLoginView.as_view()),
    path("send/sms/", basic.SendSmsView.as_view()),
    path("login/sms/", basic.SmsLoginView.as_view()),
    path("register/", basic.RegisterSmsView.as_view()),
    path("basic/", basic.BasicView.as_view()),
]
