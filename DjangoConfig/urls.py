from django.urls import path

from ApplicationSupply.views import PwdLoginView, SendSmsView, SmsLoginView

urlpatterns = [
    path("api/login/password/", PwdLoginView.as_view()),
    path("api/send/sms/", SendSmsView.as_view()),
    path("api/login/sms/", SmsLoginView.as_view()),
]
