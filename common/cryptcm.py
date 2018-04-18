# -*- coding: utf-8 -*-
# !/usr/bin/python

"""
crypt common api
加解密相关共通函数
"""

import base64
import hashlib

from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from common import logcm


def rsa_encrypt(pub_key_str, input_bytes):
    """
    按照指定的公钥字符串进行RSA加密
    @param pub_key_str: 公钥字符串
    @param input_bytes: 输入字节列表
    @return: 加密后的字节列表
    """

    # 引入公钥字符串
    pub_obj = rsa.importKey(pub_key_str)
    pub_obj = PKCS1_v1_5.new(pub_obj)

    # 执行加密
    logcm.print_info("RSA encrypt bytes : %s" % input_bytes)
    result = pub_obj.encrypt(input_bytes)

    logcm.print_obj(result, "rsa-encrypt-result", show_header=False)
    return result


def rsa_decrypt(prv_key_str, input_bytes):
    """
    按照指定的私钥字符串进行RSA解密
    @param prv_key_str: 私钥字符串
    @param input_bytes: 输入字节列表
    @return: 解密后的字节列表
    """

    # 引入私钥字符串
    prv_obj = rsa.importKey(prv_key_str)
    prv_obj = PKCS1_v1_5.new(prv_obj)

    # 执行解密
    logcm.print_info("RSA decrypt bytes : %s" % input_bytes)
    result = prv_obj.decrypt(input_bytes, '')

    logcm.print_obj(result, "rsa-decrypt-result", show_header=False)
    return result


def md5_encrypt(input_bytes):
    """
    对指定的字节列表进行MD5加密
    @param input_bytes: 输入字节列表
    @return: 加密后的字符串
    """

    # 创建md5对象
    hl = hashlib.md5()
    hl.update(input_bytes)
    logcm.print_info("MD5 encrypt bytes : %s" % input_bytes)

    # 执行加密
    result = hl.hexdigest()
    logcm.print_obj(result, "md5-encrypt-result", show_header=False)
    return result


def pad_str(input_str, padding_size, padding_char="\0"):
    """
    字符串补齐
    @param input_str: 输入字符串
    @param padding_size: 对齐宽度
    @param padding_char: 补齐字符
    @return: 补齐后的字符串
    """

    adding_num = padding_size - len(input_str) % padding_size
    suffix_str = padding_char * adding_num
    return input_str + suffix_str


def aes_encrypt(aes_key, aes_iv, input_str):
    """
    AES加密
    @param aes_key: AES秘钥KEY（长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度）
    @param aes_iv: AES-IV
    @param input_str: 输入字符串
    @return: 加密后的字符串
    """

    # 加密对象
    crypt_obj = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    logcm.print_info("AES encrypt bytes : %s" % input_str)

    # 加密后字节列表
    padded_str = pad_str(input_str, 16)
    crypt_bytes = crypt_obj.encrypt(padded_str)

    # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以这里统一把加密后的字符串转化为16进制字符串
    result = base64.b64encode(crypt_bytes)
    logcm.print_obj(result, "aes-encrypt-result", show_header=False)
    return result


def aes_decrypt(aes_key, aes_iv, input_str):
    """
    AES加密
    @param aes_key: AES秘钥KEY（长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度）
    @param aes_iv: AES秘钥IV
    @param input_str: 输入字符串
    @return: 解密后的字符串
    """

    # 加密对象
    crypt_obj = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    logcm.print_info("AES encrypt bytes : %s" % input_str)

    # 字符串转字节列表
    input_bytes = base64.b64decode(input_str)

    # 加密后字节列表
    decrypt_bytes = crypt_obj.decrypt(input_bytes)
    result = decrypt_bytes.decode("utf-8").strip('\0')

    logcm.print_obj(result, "aes-decrypt-result", show_header=False)
    return result
