from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from Components.JWT_Token import parse_payload
from Components.reponse_code import AUTHENTICATION_ERROR


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """预检不需要认证"""
        # print("before option")
        if request.method == "OPTIONS":
            return
        # 1. 读取请求头中的token
        # print("AFTER option")
        authentication = request.META.get("HTTP_AUTHORIZATION", "")

        # 2. token校验
        status, info_or_error = parse_payload(authentication)

        # 3.校验失败，返回失败信息
        if not status:
            # raise exceptions.AuthenticationFailed(
            #     {
            #         "status": "fail",
            #         "message": info_or_error,
            #         "code": AUTHENTICATION_ERROR,
            #     }
            # )
            return

            # 4. 校验成功，返回request.user  request.auth
        return info_or_error, authentication


def authenticate_header(self, request):
    """
    Return a string to be used as the value of the `WWW-Authenticate`
    header in a `401 Unauthenticated` response, or `None` if the
    authentication scheme should return `403 Permission Denied` responses.
    """
    return 'Basic realm="API"'
