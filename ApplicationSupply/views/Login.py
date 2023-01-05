from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from Components import reponse_code
from Components.JWT_Token import check_token, create_token
from Components.Serializers import PwdLoginSerializer, SmsLoginSerializer
from Database.models import Company


class PwdLoginView(APIView):
    def post(self, request, *args, **kwargs):
        ser = PwdLoginSerializer(data=request.data)
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
                "code": reponse_code.success,
                "message": "登录成功",
                "data": {"token": token, "name": instance.name},  # 返回name方便前端显示企业名称
            }
        )


class SmsLoginView(APIView):
    def post(self, request):
        # 1.接收请求数据 request.data
        # 2. 校验手机格式+手机号存在
        ser = SmsLoginSerializer(data=request.data)
        print(ser.data)
        if not ser.is_valid():
            return Response(
                {
                    "code": reponse_code.FIELD_ERROR,
                    "message": ser.errors,
                }
            )
        # 3. 获取对象
        instance = Company.objects.filter(mobile=ser.validated_data["mobile"]).first()
        # 4. 生成JWT token
        token = create_token({"user_id": instance.id, "name": instance.name})
        return Response(
            {
                "code": reponse_code.success,
                "message": "登录成功",
                "data": {"token": token, "name": instance.name},
            }
        )
