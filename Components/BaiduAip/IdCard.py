# encoding:utf-8
import base64
import pprint

import requests
from django.conf import settings


def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credential",
        "client_id": settings.ocr_api_key,
        "client_secret": settings.ocr_secret_key,
    }
    response = requests.get(url=url, params=params)
    data_dict = response.json()
    access_token = data_dict.get("access_token")
    # pprint.pprint(data_dict)
    return access_token


def ocr_path_id_card(path):
    access_token = get_token()
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard"
    f = open(path, "rb")
    img = base64.b64encode(f.read())
    params = {"id_card_side": "front", "image": img}
    request_url = request_url + "?access_token=" + access_token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(request_url, data=params, headers=headers)
    IdCardDict = response.json()
    # pprint.pprint(IdCardDict["words_result"])
    data_dict = {
        key: value["words"] for key, value in IdCardDict["words_result"].items()
    }
    # print(data_dict)
    return data_dict


if __name__ == "__main__":
    image_path = "a1.png"
    ocr_path_id_card(image_path)
