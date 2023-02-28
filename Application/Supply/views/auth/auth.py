import os
from datetime import datetime

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from Application.Database.models import CompanyAuth
from Components import reponse_code
from Components.Authentication import (
    DenyAuthentication,
    JWTAuthentication,
    JwtParamAuthentication,
)
from Components.BaiduAip.OCR_images import id_card
from Components.Mixins import CreateUpdateModelMixin, RetrieveModelMixin
from Components.Serializers import AuthModelSerializer
from DjangoConfig.settings import IdCard_key, IdCard_secret


def get_upload_filename(file_name):
    date_path = datetime.now().strftime("%Y/%m/%d")
    # 构造存储文件的目录：upload/日期/目录
    upload_path = os.path.join(settings.UPLOAD_PATH, date_path)
    # 构造文件路径
    file_path = os.path.join(upload_path, file_name)
    # 返回文件名，get_available_name会校验文件名以及重名后修改文件名
    return default_storage.get_available_name(file_path)


class AuthView(GenericViewSet, RetrieveModelMixin, CreateUpdateModelMixin):
    authentication_classes = [
        JWTAuthentication,
        JwtParamAuthentication,
        DenyAuthentication,
    ]
    queryset = CompanyAuth.objects.all()
    serializer_class = AuthModelSerializer

    @action(detail=False, methods=["post"], url_path="upload")
    def upload(self, request):
        # 获取文件对象
        upload_object = request.FILES.get("file")
        # print(upload_object.name, upload_object.size)
        upload_object.chunks(1024)
        if upload_object.size > 10 * 1024 * 1024:
            return Response({"code": reponse_code.FIELD_ERROR, "message": "文件太大"})

        upload_url = get_upload_filename(upload_object.name)
        # 保存并返回存储路径
        save_path = default_storage.save(upload_url, upload_object)
        # 返回存储得文件得url路径
        local_url = default_storage.url(save_path)
        # 当前访问的绝对url路径，后端的绝对路径，不是前端的绝对路径
        abs_url = request.build_absolute_uri(local_url)

        img_type = request.data.get("type")
        """身份证正面识别"""
        if img_type == "front":
            """读取文件数据的光标回到起始点"""
            param = {"id_card_side": "front"}
            upload_object.seek(0)
            id_info: dict = id_card(upload_object.read(), param=param)
            if id_info.get("error"):
                return Response(
                    {
                        "code": reponse_code.OCR_ERROR,
                        "message": "识别失败，请手动输入或重新上传",
                        "detail": id_info.get("detail"),
                    }
                )
            context = {
                "code": reponse_code.success,
                "type": "front",
                "data": {
                    "url": local_url,
                    "abs_url": abs_url,
                    "leader": id_info.get("姓名"),
                    "leader_identity": id_info.get("公民身份号码"),
                },
            }

        if img_type == "licence_path":
            upload_object.seek(0)
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/business_license"
            license_info: dict = id_card(upload_object.read(), new_url=request_url)
            # 2.路径返回（第三方组件） {status:1}  {status:0 }
            if license_info.get("error"):
                return Response(
                    {
                        "code": reponse_code.OCR_ERROR,
                        "message": "识别失败，请手动输入或重新上传",
                        "detail": license_info["detail"],
                    }
                )
            context = {
                "code": reponse_code.success,
                "type": "licence_path",
                "data": {
                    "url": local_url,
                    "abs_url": abs_url,
                    "title": license_info.get("单位名称"),
                    "unique_id": license_info.get("社会信用代码"),
                },
            }
        return Response(context)

    def get_instance(self):
        # 已登录的用户信息  request.user = {'user_id': instance.id, 'name': instance.name}
        user_id = self.request.user["user_id"]
        return CompanyAuth.objects.filter(company_id=user_id).first()

    def perform_create(self, serializer):
        user_id = self.request.user["user_id"]
        instance = serializer.save(company_id=user_id, remark="")
        instance.company.auth_type = 2
        instance.company.save()

    def perform_update(self, serializer):
        instance = serializer.save(remark="")
        instance.company.auth_type = 2
        instance.company.save()
