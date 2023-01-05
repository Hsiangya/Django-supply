import os

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)

# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

# 导入对应产品模块的client models。
from tencentcloud.sms.v20210111 import models, sms_client


def send_sms(phones: list, code: str, duration: str = "5"):
    try:
        cred = credential.Credential(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"))

        httpProfile = HttpProfile()
        httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
        httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
        httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
        clientProfile.language = "en-US"
        clientProfile.httpProfile = httpProfile

        client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)

        req = models.SendSmsRequest()
        req.SmsSdkAppId = os.getenv("SMS_SDK_APP_ID")
        req.SignName = os.getenv("SIGN_NAME")
        req.ExtendCode = ""
        req.SenderId = ""
        req.PhoneNumberSet = [f"+86{phone}" for phone in phones]
        req.TemplateId = os.getenv("TEMPLATE_ID")

        # req.TemplateParamSet = [code, duration]  # 依据模板内的变量决定
        req.TemplateParamSet = [code]
        resp = client.SendSms(req)
        ret = resp.to_json_string(indent=2)
        print(ret)
        return True
    except TencentCloudSDKException as err:
        print(err)
        return False
