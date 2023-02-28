from rest_framework.response import Response

from Components import reponse_code


class CreateUpdateModelMixin:
    def get_instance(self):
        """这是一个钩子，返回对象，则表示更新；返回None则表示新建"""
        pass

    def create(self, request, *args, **kwargs):
        # 1.是否认证信息已存在
        instance = self.get_instance()
        """对象存在，则执行update"""
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    {
                        "code": reponse_code.FIELD_ERROR,
                        "message": "error",
                        "detail": serializer.errors,
                    }
                )
            self.perform_update(serializer)
            return Response(
                {
                    "code": reponse_code.success,
                    "msg": "success",
                    "data": serializer.data,
                }
            )
        else:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "code": reponse_code.FIELD_ERROR,
                        "msg": "error",
                        "detail": serializer.errors,
                    }
                )
            self.perform_create(serializer)
            return Response(
                {
                    "code": reponse_code.SUCCESS,
                    "msg": "success",
                    "data": serializer.data,
                }
            )

    def perform_create(self, serializer):
        # 新增数据到数据库钩子
        serializer.save()

    def perform_update(self, serializer):
        # 扩展在数据库更新时，可以自定义字段
        serializer.save()
