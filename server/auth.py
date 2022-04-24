import os
import hashlib


def hash_new_password(password):
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, dklen=128)
    return hashed_password, salt


def verify_password(password, hashed_password, salt):
    password = password.encode('utf-8')
    # hashed_password = bytes(list(hashed_password))
    print(password, hashed_password, salt)
    new_hash = hashlib.pbkdf2_hmac('sha256', password, salt, 100000, dklen=128)
    return new_hash == hashed_password
