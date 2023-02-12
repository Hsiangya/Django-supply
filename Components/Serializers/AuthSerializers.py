from rest_framework import serializers

from Application.Database.models import CompanyAuth


class AuthModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAuth
        fields = "__all__"
