from django.urls import include, path

urlpatterns = [
    path("api/shipper/", include("Application.Supply.urls")),  # 路由分发
]
