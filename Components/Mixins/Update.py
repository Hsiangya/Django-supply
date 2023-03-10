from rest_framework.response import Response

from Components import reponse_code


class UpdateModelMixin:
    """改写UpdateModelMixin"""

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            print("1111")
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            print("11111")
            # serializer.is_valid(raise_exception=True)
            # 改写返回值
            print(instance)
            if not serializer.is_valid():
                return Response(
                    {
                        "code": reponse_code.FIELD_ERROR,
                        "message": "error",
                        "detail": serializer.errors,
                    }
                )
            print("111")
            self.perform_update(serializer)
            print("222")
            return Response(
                {
                    "code": reponse_code.success,
                    "message": "success",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            # 改写异常返回值
            return Response({"code": reponse_code.SUMMARY_ERROR, "message": "请求失败"})

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
