from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 预检直接返回response。
        if request.method == "OPTIONS":
            return HttpResponse("")

    def process_response(self, request, response):
        # 任意网址源
        response["Access-Control-Allow-Origin"] = "*"
        # 任意请求头
        response["Access-Control-Allow-Headers"] = "*"
        # 任意请求方法，解决预检
        response["Access-Control-Allow-Methods"] = "*"
        # print("Middleware")
        return response
