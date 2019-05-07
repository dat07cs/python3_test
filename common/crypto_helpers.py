import base64
import hashlib
import json
import sys

from Crypto.Cipher import AES
from Crypto.Hash import SHA
from django.conf import settings

from common import rsa_helpers, json_helpers

if sys.version_info >= (3, 0):
    def xrange(*args, **kwargs):
        return iter(range(*args, **kwargs))


def encrypt_data_rsa64(params, public_key):
    json_string = json_helpers.json_compact_dumps(params)
    data = rsa_helpers.encrypt_base64(json_string, public_key)
    return data


def decrypt_data_rsa64(encrypted_data, private_key):
    json_string = rsa_helpers.decrypt_base64(encrypted_data, private_key)
    data = json.loads(json_string)
    return data


def sign_data_rsa64(params, private_key, binary=False, hash_method=SHA):
    json_string = json_helpers.json_compact_dumps(params)
    sign = rsa_helpers.sign_data(json_string, private_key, hash_method)
    if binary:
        return sign
    return sign.decode('ascii')


def verify_data_rsa64(params, public_key, sign, hash_method=SHA):
    json_string = json_helpers.json_compact_dumps(params)
    return rsa_helpers.verify_data(json_string, public_key, sign, hash_method)


AES_BLOCK_SIZE = 16
AES_CBC_IV = b'\0' * AES_BLOCK_SIZE


def aes_cbc_encrypt(data, key):
    if not isinstance(key, bytes):
        key = key.encode('utf-8')
    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    return AES.new(key, AES.MODE_CBC, AES_CBC_IV).encrypt(data)


def aes_cbc_decrypt(data, key):
    if not isinstance(key, bytes):
        key = key.encode('utf-8')
    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    try:
        return AES.new(key, AES.MODE_CBC, AES_CBC_IV).decrypt(data)
    except:
        return None


def pkcs7_padding(data, block_size):
    pad = block_size - (len(data) % block_size)
    data += chr(pad) * pad
    return data


def pkcs7_unpadding(data, block_size):
    size = len(data)
    if size < block_size or size % block_size != 0:
        return None
    pad = ord(data[-1])
    if pad <= 0 or pad > block_size:
        return None
    for i in xrange(2, pad + 1):
        if ord(data[-i]) != pad:
            return None
    return data[:-pad]


def aes_cbc_pkcs7_encrypt(plaintext, encryption_key):
    padded_data = pkcs7_padding(plaintext, AES_BLOCK_SIZE)
    encrypted_data = aes_cbc_encrypt(padded_data, encryption_key)
    return base64.b64encode(encrypted_data).decode('utf-8')


def aes_cbc_pkcs7_decrypt(data, encryption_key):
    base64_decoded_data = base64.b64decode(data)
    decrypted_data = aes_cbc_decrypt(base64_decoded_data, encryption_key).decode('utf-8')
    return pkcs7_unpadding(decrypted_data, AES_BLOCK_SIZE)


class CardNoHelper(object):
    @classmethod
    def encrypt(cls, card_number, one_way_encryption=False):
        if one_way_encryption is True:
            return md5_string(card_number)
        return aes_cbc_pkcs7_encrypt(card_number, settings.CARD_NO_ENCRYPTION_KEY)

    @classmethod
    def decrypt(cls, encrypted_card_number):
        try:
            return aes_cbc_pkcs7_decrypt(encrypted_card_number, settings.CARD_NO_ENCRYPTION_KEY)
        except:
            raise ValueError('%s is invalid data for decryption' % encrypted_card_number)

    @classmethod
    def verify(cls, card_number, encrypted_card_number, one_way_encryption=False):
        return encrypted_card_number == cls.encrypt(card_number, one_way_encryption)

    @classmethod
    def mask_card_number(cls, card_number):
        if not card_number:
            return card_number
        length = len(card_number)
        if length < 16:
            masked_card_number = ('x' * (length - 4)) + card_number[-4:]
        else:
            masked_card_number = card_number[:6] + ('x' * (length - 10)) + card_number[-4:]
        return masked_card_number


class PKCS7Encoder(object):
    def __init__(self, k=16):
        self.k = k

    # @param bytestring    The padded bytestring for which the padding is to be removed.
    # @exception ValueError Raised when the input padding is missing or corrupt.
    # @return bytestring    Original unpadded bytestring.
    def decode(self, bytestring):
        """
        Remove the PKCS#7 padding from a text bytestring.

        """

        val = bytestring[-1]
        if val > self.k:
            raise ValueError('Input is not padded or padding is corrupt')
        return bytestring[:len(bytestring) - val]

    # @param bytestring    The text to encode.
    # @return bytestring    The padded bytestring.
    def encode(self, bytestring):
        """
        Pad an input bytestring according to PKCS#7

        """
        val = self.k - (len(bytestring) % self.k)
        return bytestring + bytearray([val] * val)


def md5_string(data, upper=False, unicode=True):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    hashed_string = m.hexdigest()
    if not unicode:
        hashed_string = hashed_string.encode('utf-8')
    if upper:
        return hashed_string.upper()
    return hashed_string
