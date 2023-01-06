import random

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from Components import TencentSendSms, reponse_code
from Components.Serializers import SendSmsSerializer


class SendSmsView(APIView):
    def post(self, request):
        try:
            ser = SendSmsSerializer(data=request.data)
            if not ser.is_valid():
                return Response(
                    {
                        "code": reponse_code.FIELD_ERROR,
                        "message": ser.errors,
                        "status": "fail",
                    }
                )
            random_code = str(random.randint(1000, 9999))
            # print(ser.validated_data["mobile"])
            # print(random_code)
            # 腾讯云短信接口发送短信
            phones_list = [ser.validated_data["mobile"]]
            TencentSendSms.send_sms(phones_list, random_code, duration="5")
            conn = get_redis_connection("default")
            conn.set(ser.validated_data["mobile"], random_code, ex=300)
            # 5.返回
            return Response(
                {
                    "code": reponse_code.success,
                    "status": "success",
                    "message": "短信验证码已发送",
                }
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "code": reponse_code.SUMMARY_ERROR,
                    "status": "fail",
                    "message": "短信验证码发送失败",
                }
            )
