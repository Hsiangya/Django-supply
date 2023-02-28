from rest_framework import serializers

from Application.Database.models import Company, CompanyAuth


class AuthModelSerializer(serializers.ModelSerializer):
    """认证文字信息"""

    auth_type_text = serializers.CharField(
        source="company.get_auth_type_display", read_only=True
    )
    auth_type_class = serializers.SerializerMethodField(read_only=True)

    """编辑页面的预览完整地址"""
    licence_path_url = serializers.SerializerMethodField()
    leader_identity_front_url = serializers.SerializerMethodField()
    leader_identity_back_url = serializers.SerializerMethodField()

    class Meta:
        model = CompanyAuth
        # fields = "__all__"
        exclude = ["company"]
        # extra_kwargs = {
        #     'remark': {"read_only": True}
        # }

    def get_auth_type_class(self, obj):
        """通过auth_type匹配返回认证样式的信息"""
        return Company.auth_type_class_map[obj.company.auth_type]

    #
    def get_licence_path_url(self, obj):
        # get_serializer_class中设定了context值，可以获取request对象
        # abs_url = request.build_absolute_uri(local_url)
        return self.context["request"].build_absolute_uri(obj.licence_path)

    def get_leader_identity_front_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.leader_identity_front)

    def get_leader_identity_back_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.leader_identity_back)
