from django.core.validators import RegexValidator
from django_redis import get_redis_connection
from rest_framework import exceptions, serializers

from Components.encrypt import md5
from Database.models import Company


class PwdLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_password(self, value):
        md5_string = md5(value)
        return md5_string


class SmsLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        required=True, validators=[RegexValidator(r"\d{11}", message="格式错误")]
    )
    code = serializers.CharField(
        required=True, validators=[RegexValidator(r"\d{4}", message="格式错误")]
    )

    def validate_mobile(self, value):
        is_exists = Company.objects.filter(mobile=value).exists()
        if not is_exists:
            raise exceptions.ValidationError("手机未注册")
        return value

    def validate_code(self, value):
        mobile = self.initial_data.get("mobile")
        connect = get_redis_connection("default")
        cache_code = connect.get(mobile)
        if not cache_code:
            raise exceptions.ValidationError("验证码不存在或已过期")
        cache_code = cache_code.decode("utf-8")
        if cache_code != value:
            raise exceptions.ValidationError("验证码错误")
        connect.delete(mobile)
        return value
