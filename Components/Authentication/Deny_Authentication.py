from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class DenyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        raise exceptions.AuthenticationFailed({"code": 8888, "message": "认证失败"})

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'API realm="API"'
