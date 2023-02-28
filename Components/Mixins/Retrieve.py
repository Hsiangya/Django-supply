from django.http.response import Http404
from rest_framework.response import Response

from Components import reponse_code


class RetrieveModelMixin:
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({"code": reponse_code.success, "data": serializer.data})
        except Http404 as e:
            return Response(
                {
                    "code": reponse_code.NOT_FOUND_FIELD,
                    "message": "对象不存在",
                }
            )
        except Exception as e:
            return Response(
                {
                    "code": reponse_code.SUMMARY_ERROR,
                    "message": "请求失败",
                }
            )
