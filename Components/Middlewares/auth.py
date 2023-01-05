from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # 任意网址源
        response["Access-Control-Allow-Origin"] = "*"
        # 任意请求头
        response["Access-Control-Allow-Headers"] = "*"
        # 任意请求方法，解决预检
        response["Access-Control-Allow-Methods"] = "*"
        return response
