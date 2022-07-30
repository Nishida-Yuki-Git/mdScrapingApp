from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os

class CipClassSingleton(object):
    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

class Decrypt(CipClassSingleton):
    def __init__(self):
        self.key_file_path = '../../cip_key.txt'
        self.decodeCharset = 'utf-8'
        self.key_file_data = self.__readKeyFile()
        self.key = self.key_file_data[0]
        self.iv = self.key_file_data[1]

    def __readKeyFile(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open(self.key_file_path) as file:
            file_data = [s.strip() for s in file.readlines()]
        return file_data

    def decryptMethod(self, targetCode):
        ct = b64decode(targetCode)
        print(targetCode)
        print(self.key.encode(self.decodeCharset))
        print(self.iv.encode(self.decodeCharset))
        cipher = AES.new(key=self.key.encode(self.decodeCharset),
                         mode=AES.MODE_CBC,
                         iv=self.iv.encode(self.decodeCharset))
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode(self.decodeCharset)

