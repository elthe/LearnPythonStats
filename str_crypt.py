#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
加解密使用示例。
"""

from common import cryptcm
from common import filecm
from common import checkcm

# 缓存目录
cache_path = './cache/crypt'
pub_key_file = 'public.key'
prv_key_file = 'private.key'
input_str = "{key:1234}"

# 公私钥字符串
pub_key_str = filecm.read_str(cache_path, pub_key_file, "utf-8")
prv_key_str = filecm.read_str(cache_path, prv_key_file, "utf-8")

# RSA加密
input_bytes = input_str.encode("utf-8")
encrypt_bytes = cryptcm.rsa_encrypt(pub_key_str, input_bytes)

# RSA解密
decrypt_bytes = cryptcm.rsa_decrypt(prv_key_str, encrypt_bytes)

# 确定解密后和加密前是否一致
checkcm.check_equal(input_bytes, decrypt_bytes, "decrypt bytes")

# MD5加密
md5_str = cryptcm.md5_encrypt(input_bytes)

# AES加密
aes_key = "1234567812345678"
aes_iv = "1234567812345678"
encrypt_str = cryptcm.aes_encrypt(aes_key, aes_iv, input_str)

# AES解密
decrypt_str = cryptcm.aes_decrypt(aes_key, aes_iv, encrypt_str)

# 确定解密后和加密前是否一致
checkcm.check_equal(input_str, decrypt_str, "AES decrypt string")
