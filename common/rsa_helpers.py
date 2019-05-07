import logging
import base64
import sys
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_v1_5_signer
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_cipher
from random import Random

from common.utility_helpers import format_exc_info

logger = logging.getLogger('main')


def import_key(file_path):
    """
    Import RSA key, can use for both public key and private key
    :param file_path: path to your key
    :return: RSA object
    """
    with open(file_path, 'r') as fh:
        return RSA.importKey(fh.read())


def import_key_from_string(key_content):
    try:
        return RSA.importKey(key_content)
    except:
        return None


def encrypt_base64(data, public_key):
    """
    Encrypt data with public key then encode base 64 data into hex string
    :param data: data to be encrypted
    :param public_key: RSA object key
    :return: base 64 string
    """
    hash_object = SHA.new(data)
    cipher = PKCS1_v1_5_cipher.new(public_key)
    encrypted = cipher.encrypt(data + hash_object.digest())
    return base64.b64encode(encrypted)


def decrypt_base64(data, private_key):
    """
    Decode base 64 string and decrypt with private key
    :param data: base 64 string
    :param private_key: RSA object key
    :return: data
    """
    data = base64.b64decode(data)
    digest_size = SHA.digest_size
    sentinel = Random.new().read(8 + digest_size)
    cipher = PKCS1_v1_5_cipher.new(private_key)
    message = cipher.decrypt(data, sentinel)
    return message[:-digest_size]


def sign_data(data, private_key, hash_method=SHA, base64encode=True):
    """
    Sign data with private key then encode base64 signature
    :param data: data with be signed
    :param private_key: RSA object key
    :param hash_method: hash method in Crypto.Hash module, default is SHA
    :param base64encode: encode base64 or not
    :return: base 64 string of signature
    """
    # logger.info('sign_data | data: %s | hash_method', data, hash_method)
    signer = PKCS1_v1_5_signer.new(private_key)
    hash_object = hash_method.new(data.encode('utf8'))
    sign = signer.sign(hash_object)

    if base64encode:
        return base64.b64encode(sign)
    return sign


def verify_data(data, public_key, signature, hash_method=SHA, base64encode=True):
    """
    Verify signature
    :param data: data to verify
    :param public_key: RSA object ket
    :param signature: base 64 string to compare
    :param hash_method: hash method in Crypto.Hash module, default is SHA
    :param base64encode: decode base64 or not
    :return: True of False
    """
    # logger.info('verify_data | data: %s | hash_method: %s', data, hash_method)
    try:
        verifier = PKCS1_v1_5_signer.new(public_key)
        hash_object = hash_method.new(data.encode('utf8'))
        if base64encode:
            signature = base64.b64decode(signature)
        return verifier.verify(hash_object, signature)
    except:
        exc_info = sys.exc_info()
        logging.error('Data: {} | Sign: {} | Exception: {}'.format(data, signature, format_exc_info(exc_info)))
    return False
