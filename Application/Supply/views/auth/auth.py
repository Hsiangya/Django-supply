import os
from datetime import datetime

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Application.Database.models import Company
from Components import reponse_code
from Components.Serializers import AuthModelSerializer


def get_upload_filename(file_name):
    date_path = datetime.now().strftime("%Y/%m/%d")
    # 构造存储文件的目录：upload/日期/目录
    upload_path = os.path.join(settings.UPLOAD_PATH, date_path)
    # 构造文件路径
    file_path = os.path.join(upload_path, file_name)
    # 返回文件名，get_available_name会校验文件名以及重名后修改文件名
    return default_storage.get_available_name(file_path)


def baidu_ai(bytes_body):
    import base64

    import requests

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    response = requests.get(
        url="https://aip.baidubce.com/oauth/2.0/token",
        params={
            "grant_type": "client_credentials",
            "client_id": "PhGc5UK5e5UOkSqpNakZLpxL",
            "client_secret": "cS1OaU3GngGDdsZj2Fo7scd4j7S3M3Gw",
        },
    )
    data_dict = response.json()
    access_token = data_dict["access_token"]
    # print(access_token)

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard"
    # 二进制方式打开图片文件
    img = base64.b64encode(bytes_body)

    params = {"id_card_side": "front", "image": img}  # front/back
    request_url = request_url + "?access_token=" + access_token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    res = requests.post(request_url, data=params, headers=headers)
    res_dict = res.json()
    for k, v in res_dict["words_result"].items():
        print(k, v)


class AuthView(ModelViewSet):
    queryset = Company.objects.all()
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
        if img_type == "front":
            upload_object.seek(0)
            baidu_ai(upload_object.read())

        context = {
            "code": reponse_code.success,
            "data": {"url": local_url, "abs_url": abs_url},
        }
        # 2.路径返回（第三方组件） {status:1}  {status:0 }
        return Response(context)
