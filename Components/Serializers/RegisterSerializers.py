from django.core.validators import RegexValidator
from rest_framework import exceptions, serializers

from Application.Database.models import Company
from Components.encrypt import md5


class RegisterSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(
        required=True, validators=[RegexValidator(r"\d{11}", message="手机号格式错误")]
    )
    code = serializers.CharField(
        required=True, validators=[RegexValidator(r"\d{4}", message="验证码格式错误")]
    )
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = Company
        fields = ["name", "mobile", "code", "password", "confirm_password"]

    def validate_mobile(self, value):
        # 自定义验证
        exists = Company.objects.filter(mobile=value).exists()
        if exists:
            raise exceptions.ValidationError("手机号已注册")
        return value

    def validate_password(self, value):
        return md5(value)

    def validate_confirm_password(self, value):
        password = self.initial_data.get("password")
        if value != password:
            raise exceptions.ValidationError("密码不一致")
        return value


class RegisterSmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        required=True, validators=[RegexValidator(r"\d{11}", message="格式错误")]
    )

    def validate_mobile(self, value):
        # 自定义验证
        exists = Company.objects.filter(mobile=value).exists()
        if exists:
            raise exceptions.ValidationError("手机已注册")
        return value
