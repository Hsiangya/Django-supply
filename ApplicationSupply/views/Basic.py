from rest_framework.response import Response
from rest_framework.views import APIView

from Components.Authentication import JWTAuthentication
from Components.reponse_code import success


class BasicView(APIView):
    authentication_classes = [
        JWTAuthentication,
    ]

    def get(self, request):
        print(request.data)
        print(request.user)
        print(request.auth)
        return Response({"status": "success", "code": success, "message": "访问成功"})
