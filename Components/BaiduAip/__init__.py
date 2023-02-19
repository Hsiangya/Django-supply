import requests

from .image_path import image_ocr

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
