from Crypto.Cipher import *

def encrypt(plain_text='', key=''):
    des = DES.new(key)
    cipher_text = des.encrypt(plain_text)

    return cipher_text


def decrypt(cipher_text='', key=''):
    des = DES.new(key)
    message = des.decrypt(cipher_text)

    return message