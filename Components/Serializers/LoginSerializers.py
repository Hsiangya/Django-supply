from rest_framework import serializers

from Components.encrypt import md5


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_password(self, value):
        md5_string = md5(value)
        return md5_string
