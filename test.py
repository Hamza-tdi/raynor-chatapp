import os

from cryptography.fernet import Fernet
from passlib.hash import pbkdf2_sha256
# WD_PATH = os.path.dirname(os.path.realpath(__file__))
# encrypt_file = fr'{WD_PATH}\encryption_key'
# if not os.path.isfile(encrypt_file):
#     key = Fernet.generate_key()
#     with open('encryption_key', 'wb') as f:
#         f.write(key)
# else:
#     with open('encryption_key', 'rb') as f:
#         key = f.read()
#
#
# message = 'hello'
# f = Fernet(key)
#
# cypted_msg = f.encrypt(message.encode())
# print(cypted_msg)
# decrypted_msg = f.decrypt(cypted_msg)
# print(decrypted_msg)

password = 'ADMIN'
hashed = pbkdf2_sha256.hash(password)
print(hashed)