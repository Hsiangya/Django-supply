# encoding:utf-8

import base64

import requests
from django.conf import settings

from . import get_token


def image_ocr(path, request_url, aip_key, aip_secret, params_data=None):
    """
    :param path: 图片地址
    :param request_url: 请求的url
    :param params_data: 需要额外添加的请求参数
    营业执照需要添加params_data
    :return: 识别的数据键值对
    """
    access_token = get_token(aip_key, aip_secret)
    """读取图片并进行base64编码  add"""
    f = open(path, "rb")
    img = base64.b64encode(f.read())
    params = {"image": img}
    if params_data:
        params.update(params_data)
    request_url = request_url + "?access_token=" + access_token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(request_url, data=params, headers=headers).json()
    data_dict = {
        key: value["words"] for key, value in response["words_result"].items()
    }
    return data_dict
