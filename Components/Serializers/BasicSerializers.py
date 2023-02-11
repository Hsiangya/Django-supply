from django.core.validators import RegexValidator
from rest_framework import exceptions, serializers

from Application.Database.models import Company


class BasicModelSerializer(serializers.ModelSerializer):
    """序列化返回的基本信息"""

    mobile = serializers.SerializerMethodField()  # 自定义序列化手机号格式
    ctime = serializers.DateTimeField(format="%Y-%m-%d")  # 自定义序列化时间格式
    auth_type_text = serializers.CharField(source="get_auth_type_display")  # 自定义认证类型的文字

    class Meta:
        model = Company
        fields = ["id", "name", "mobile", "ctime", "auth_type", "auth_type_text"]

    def get_mobile(self, object):
        """请求钩子、自定义手机格式"""
        return object.mobile[0:3] + "****" + object.mobile[-4:]


class NameModelSerializer(serializers.ModelSerializer):
    """序列化返回单个名字"""

    class Meta:
        model = Company
        fields = ["name"]


class MobileModelSerializer(serializers.ModelSerializer):
    """序列化返回单个手机号"""

    class Meta:
        model = Company
        fields = ["old", "mobile", "new_mobile"]
        extra_kwargs = {
            "old": {"validators": [RegexValidator(r"\d{11}", message="手机格式错误")]},
            "mobile": {
                "validators": [
                    RegexValidator(r"\d{11}", message="手机格式错误"),
                ],
                "write_only": True,
            },
        }

    def validate_old(self, val):
        # 当前登录用的手机号是不是
        request = self.context["request"]
        user_id = request.user["user_id"]
        exists = Company.objects.filter(id=user_id, mobile=val).exists()
        if not exists:
            raise exceptions.ValidationError("原手机号错误")
        return val

    def get_new_mobile(self, obj):
        return obj.mobile[0:3] + "****" + obj.mobile[-4:]
