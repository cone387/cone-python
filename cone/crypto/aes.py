# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2022/3/20 下午4:31
# software: PyCharm

# from Crypto.Cipher import AES
# from Crypto import Random
# import base64
# import msvcrt, sys


class AESEncrypt(object):
    def __init__(self, key):
        self.key = key

    def format_key(cls, key):
        sub_key = '*' * (16 - len(key))
        key += sub_key
        return key

    def padding(cls, s):
        pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(0) #chr(AES.block_size - len(s) % AES.block_size)
        return pad(s)

    def unpadding(cls, s):
        # unpad = lambda s : s[:-ord(s[len(s)-1:])]
        unpad = lambda s: s.rstrip(chr(0))
        return unpad(s)

    def encrypt(cls, text, key=None):
        # key = cls.key if not key else cls.format_key(key)
        # text = AESEncrypter.padding(text)
        # iv = Random.new().read(AES.block_size)
        # cryptor = AES.new(key, AES.MODE_CBC, iv)
        # result = base64.b64encode(iv + cryptor.encrypt(text))
        return result.decode()

    def decrypt(cls, text, key=None):
        pass


def encrypt(key, ):
    return AESEncrypt(key).encrypt()