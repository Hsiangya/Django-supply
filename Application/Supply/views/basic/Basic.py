from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from Application.Database.models import Company
from Components.Authentication import JWTAuthentication
from Components.Mixins import RetrieveModelMixin, UpdateModelMixin
from Components.reponse_code import success


class BasicView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    authentication_classes = [
        JWTAuthentication,
    ]  # 认证信息
    queryset = Company.objects.all()

    def get(self, request):
        print(request.data)
        print(request.user)
        print(request.auth)
        return Response({"status": "success", "code": success, "message": "访问成功"})
