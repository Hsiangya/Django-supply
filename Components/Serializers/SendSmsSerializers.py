from django.core.validators import RegexValidator
from rest_framework import exceptions, serializers

from Application.Database.models import Company


class SendSmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        required=True, validators=[RegexValidator(r"\d{11}", message="格式错误")]
    )

    def validate_mobile(self, value):
        # 自定义验证
        exists = Company.objects.filter(mobile=value).exists()
        if not exists:
            raise exceptions.ValidationError("手机未注册")
        return value
