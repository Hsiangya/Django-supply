from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from Application.Database.models import Company
from Components.Authentication import JWTAuthentication
from Components.Filter import BasicIDFilter
from Components.Mixins import RetrieveModelMixin, UpdateModelMixin
from Components.Serializers import (
    BasicModelSerializer,
    MobileModelSerializer,
    NameModelSerializer,
)


class BasicView(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    authentication_classes = [
        JWTAuthentication,
    ]  # 认证信息
    filter_backends = [BasicIDFilter]
    queryset = Company.objects.all()
    serializer_class = BasicModelSerializer

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            req_type = self.request.query_params.get("type")
            if req_type == "name":
                return NameModelSerializer
            elif req_type == "mobile":
                return MobileModelSerializer
        return BasicModelSerializer
