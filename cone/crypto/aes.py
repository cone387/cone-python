try:
    from Crypto.Cipher import AES
except ImportError:
    raise ImportError("Please install pycryptodome first, pip install pycryptodome")
from Crypto import Random
import base64
from enum import StrEnum


class Padding(StrEnum):
    ZERO = 'ZERO'
    PKCS7 = 'PKCS7'
    PKCS5 = 'PKCS5'
    ISO10126 = 'ISO10126'
    ANSI_X923 = 'ANSI_X923'
    NO_PADDING = 'NO_PADDING'


class AESEncrypter(object):
    def __init__(self, key: str, mode=AES.MODE_CBC, padding=Padding.ZERO, iv=None):
        self.key = self.padding(key, padding).encode()
        self.mode = mode
        self.padding_mode = padding
        if iv is not None:
            if isinstance(iv, str):
                iv = iv.encode()
        self.iv = iv

    @staticmethod
    def padding(string: str, padding=Padding.ZERO) -> str:
        num = (AES.block_size - len(string) % AES.block_size)
        if padding == Padding.ZERO:
            string = string + num * chr(0)
        elif padding == Padding.PKCS7:
            string = string + num * chr(num)
        elif padding == Padding.PKCS5:
            string = string + num * chr(num)
        elif padding == Padding.ISO10126:
            string = string + num * chr(num)
        elif padding == Padding.ANSI_X923:
            string = string + num * chr(num)
        elif padding == Padding.NO_PADDING:
            string = string
        else:
            raise ValueError("Invalid padding mode")
        return string

    @staticmethod
    def unpadding(string: str, padding_char=Padding.ZERO) -> str:
        if padding_char == Padding.ZERO:
            return string.rstrip(chr(0))
        return string

    def encrypt(self, string: str):
        string = AESEncrypter.padding(string, self.padding_mode)
        iv = self.iv or Random.new().read(AES.block_size)
        cipher = AES.new(self.key, self.mode, iv)
        result = base64.b64encode(iv + cipher.encrypt(string.encode()))
        return result.decode()

    def decrypt(self, string: str):
        # ValueError: Incorrect IV length (it must be 16 bytes long)
        string = base64.b64decode(string)
        iv = string[:AES.block_size]
        cipher = AES.new(self.key, self.mode, iv)
        result = cipher.decrypt(string[len(iv):])
        result = AESEncrypter.unpadding(result.decode(), self.padding_mode)
        return result


def encrypt(string, key, mode=AES.MODE_CBC, iv=None, padding=Padding.ZERO):
    return AESEncrypter(key, mode, padding, iv).encrypt(string)


def decrypt(string, key, mode=AES.MODE_CBC, iv=None, padding=Padding.ZERO):
    return AESEncrypter(key, mode, padding, iv).decrypt(string)


if __name__ == '__main__':
    text = "这是一段加密内容"
    print("加密前的内容：", text)
    s = encrypt(text, '123456', iv='1234567890123456')
    print("加密后的内容：", s)
    print("解密后的内容：", decrypt(s, '123456', iv='1234567890123456'))

