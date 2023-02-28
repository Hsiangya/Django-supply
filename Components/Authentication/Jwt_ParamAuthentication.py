from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from Components.JWT_Token import parse_payload


class JwtParamAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        # 1.读取请求头中的token
        authorization = request.query_params.get("token")

        # 2.token校验
        status, info_or_error = parse_payload(authorization)

        # 3.校验失败，继续往后走
        if not status:
            return

        # 4.校验成功，继续向后  request.user  request.auth
        return info_or_error, authorization

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'API realm="API"'
