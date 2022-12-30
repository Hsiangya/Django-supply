from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from Components.Serializers import LoginSerializer
from Database.models import Company


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        ser = LoginSerializer(data=request.data)
        print(request.data)
        if not ser.is_valid():
            return Response(
                {
                    "status": "fail",
                    "code": 1001,
                    "message": "校验失败",
                    "detail": ser.errors,
                }
            )
        instance = Company.objects.filter(**ser.data).first()
        if not instance:
            return Response({"status": "fail", "code": 1001, "message": "账号或密码不正确"})

        return Response({"status": "success", "code": 1000, "message": "登录成功"})
