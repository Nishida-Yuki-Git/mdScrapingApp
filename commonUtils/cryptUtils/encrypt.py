##運用上しか使用しない暗号化部品

from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

plane_data = "".encode('utf-8')
key = "".encode('utf-8')
iv = "".encode('utf-8')

en_cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
en_ct_bytes = en_cipher.encrypt(pad(plane_data, AES.block_size))
ct = b64encode(en_ct_bytes).decode('utf-8')

print(ct)