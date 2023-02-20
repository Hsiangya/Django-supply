import base64

import requests
from django.conf import settings

from DjangoConfig.settings import IdCard_key, IdCard_secret

token_url = "https://aip.baidubce.com/oauth/2.0/token"


def get_token(api_key, api_secret, url=token_url):
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret,
    }
    response = requests.get(url=url, params=params)
    access_token = response.json().get("access_token")
    return access_token


def id_card(image, param=None, new_url=None):
    try:
        access_token = get_token(IdCard_key, IdCard_secret)
        """读取图片并进行base64编码  """
        # f = open(path, "rb")
        img = base64.b64encode(image)
        params = {"image": img}
        if param:
            params = {"image": img, **param}
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard"
        if new_url:
            url = new_url
        request_url = url + "?access_token=" + access_token
        headers = {"content-type": "application/x-www-form-urlencoded"}

        response = requests.post(request_url, data=params, headers=headers).json()
        data_dict = {
            key: value["words"] for key, value in response["words_result"].items()
        }
    except Exception as e:
        data_dict = {"error": "识别失败", "detail": e}
    return data_dict
