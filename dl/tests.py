from django.test import TestCase
import operator

# Create your tests here.

# -*- coding=utf-8
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = 'AKIDb0mJgpST0VotkQd490reHgrqa2HJQg17'  # 替换为用户的 secretId
secret_key = '1qjW5PYS7XjhgV2LSK1Zv76qLdcMvGao'  # 替换为用户的 secretKey
region = 'ap-guangzhou'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)

Bucket = 'wonder-1300427053'

if __name__ == '__main__':
    bucket_list = client.list_objects(
        Bucket=Bucket,
        Prefix='iOS_Log/',
        MaxKeys=1
    )
    print(bucket_list['Contents'][0]['Key'])
