import datetime

import jwt
from django.conf import settings
from jwt import exceptions

# SALT = 'iv%x6xo7l7_u9bf_u!9#g#m*)*=ej@bek5)(@u3kh*72+unjv='


def parse_payload(token):
    try:
        # 从token中获取payload【不校验合法性】
        # unverified_payload = jwt.decode(token, None, False)
        # print(unverified_payload)

        # 从token中获取payload【校验合法性】
        verified_payload = jwt.decode(
            token, settings.JWT_KEY.encode("utf-8"), algorithms=["HS256"]
        )
        return True, verified_payload
    except exceptions.ExpiredSignatureError:
        error = "token已失效"
    except jwt.DecodeError:
        error = "token认证失败"
    except jwt.InvalidTokenError:
        error = "非法的token"
    return False, error


if __name__ == "__main__":
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6Imp3dCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Ind1cGVpcWkiLCJleHAiOjE2Njk1NDM2Nzd9.i7A8yQZo2CWvot_BbDwDKf8fdHQ-XymTY9W0ss1plvM"
    payload = parse_payload(token)
    print(payload)
