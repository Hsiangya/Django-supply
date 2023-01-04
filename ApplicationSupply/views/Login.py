from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from Components.JWT_Token import check_token, create_token
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
        "写入token"
        token = create_token({"user_id": instance.id, "name": instance.name})
        return Response(
            {
                "status": "success",
                "code": 1000,
                "message": "登录成功",
                "data": {"token": token, "name": instance.name},  # 返回name方便前端显示企业名称
            }
        )
