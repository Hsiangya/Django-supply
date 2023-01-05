from django.urls import path

from ApplicationSupply.views import PwdLoginView, SmsLoginView

urlpatterns = [
    path("api/login/", PwdLoginView.as_view()),
    path("api/login/", PwdLoginView.as_view()),
]
