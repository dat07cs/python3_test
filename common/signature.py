from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
import base64


def import_rsa_key(key_file):
    content = open(key_file).read()
    return RSA.importKey(content)


def sign(rsa_pri_key_file, data, hash_method=SHA, b64encode=True):
    rsa_pri_key = open(rsa_pri_key_file).read()
    return sign_by_key(rsa_pri_key, data, hash_method, b64encode)


def verify(rsa_pub_key_file, data, sig, hash_method=SHA, b64encode=True):
    rsa_pub_key = open(rsa_pub_key_file).read()
    return verify_by_key(rsa_pub_key, data, sig, hash_method, b64encode)


def sign_by_key(rsa_pri_key, data, hash_method=SHA, b64encode=True):
    rsa_pri_key = RSA.importKey(rsa_pri_key)
    sig_maker = PKCS1_v1_5.new(rsa_pri_key)
    h = hash_method.new(data.encode('utf-8'))
    sig = sig_maker.sign(h)
    if b64encode:
        sig = base64.b64encode(sig)
    return sig


def verify_by_key(rsa_pub_key, data, sig, hash_method=SHA, b64encode=True):
    rsa_pub_key = RSA.importKey(rsa_pub_key)
    verifier = PKCS1_v1_5.new(rsa_pub_key)
    h = hash_method.new(data.encode('utf-8'))
    if b64encode:
        sig = base64.b64decode(sig)
    return verifier.verify(h, sig)
