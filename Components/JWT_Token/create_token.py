import datetime

import jwt
from django.conf import settings
from jwt import exceptions

# SALT = 'iv%x6xo7l7_u9bf_u!9#g#m*)*=ej@bek5)(@u3kh*72+unjv='


def create_token(payload, timeout=1):
    # 构造header，即第一段信息
    headers = {"typ": "jwt", "alg": "HS256"}

    # 构造payload，第二段用户信息
    # payload = {
    #     'user_id': 1,  # 自定义用户ID
    #     'username': 'hsiangya',  # 自定义用户名
    #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)  # 超时时间
    # }
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=timeout)

    # 生成JWT Token
    result = jwt.encode(
        payload=payload,
        key=settings.JWT_KEY.encode("utf-8"),
        algorithm="HS256",
        headers=headers,
    )

    # 返回结果
    return result


if __name__ == "__main__":
    # eyJhbGciOiJIUzI1NiIsInR5cCI6Imp3dCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Ind1cGVpcWkiLCJleHAiOjE2Njk1NDM2Nzd9.i7A8yQZo2CWvot_BbDwDKf8fdHQ-XymTY9W0ss1plvM
    token = create_token()
    print(token)
