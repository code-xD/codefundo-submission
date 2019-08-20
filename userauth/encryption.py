from cryptography.fernet import Fernet
import base64
import string
import random


def gen2key():
    letters = string.ascii_letters
    strmessage = ''.join(random.choice(letters)
                         for i in range(32))
    message = strmessage.encode()
    private_key = ''.join(random.choice(letters)
                          for i in range(32))
    key = base64.urlsafe_b64encode(private_key.encode())
    f = Fernet(key)
    encrypted = f.encrypt(message)
    strencryp = encrypted.decode('utf-8')
    return [private_key, strencryp, strmessage]


def genspkey(private_key):
    letters = string.ascii_letters
    strmessage = ''.join(random.choice(letters)
                         for i in range(32))
    message = strmessage.encode()
    key = base64.urlsafe_b64encode(private_key.encode())
    f = Fernet(key)
    encrypted = f.encrypt(message)
    strencryp = encrypted.decode('utf-8')
    return [strmessage, strencryp]


def decrypt(private_key, encrypted_string, org_string):
    key = base64.urlsafe_b64encode(private_key.encode())
    f = Fernet(key)
    binencryp = encrypted_string.encode()
    decryp = f.decrypt(binencryp)
    decryp = decryp.decode('utf-8')
    return org_string == decryp
