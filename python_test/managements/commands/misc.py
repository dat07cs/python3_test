import base64
import os

import re
import threading
from io import StringIO
from time import sleep

import requests
import struct
from Crypto import Signature
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from django.core.management.base import BaseCommand

from common import json_helpers


class Command(BaseCommand):
    def handle(self, *args, **options):
        def performance_test():
            url = 'http://127.0.0.1:8000/check_balance/'
            # url = 'http://dev-giro.airpay.vn/check_balance/'
            bank_id = 6

            reply = requests.post(url, data={'bank_id': bank_id}, timeout=60)
            if reply.status_code != 200:
                print(reply.status_code, reply.headers['X-Request-ID'])

        # while True:
        #     threading.Thread(target=performance_test).start()
            # threading.Thread(target=performance_test).start()
            # threading.Thread(target=performance_test).start()
            # threading.Thread(target=performance_test).start()
            # threading.Thread(target=performance_test).start()
            # sleep(1)
        #
        # x = 5 * 60
        # y = 60
        # x = y = 1
        # for _ in xrange(x):
        #     for _ in xrange(y):
        #         threading.Thread(target=performance_test).start()
        #     sleep(1)

        def unescape(s):
            print(s.replace('&lt;', '<').replace('&gt;', '>'))

        unescape('&lt;RESPONSE&gt;&lt;RESPONSECODE&gt;02&lt;/RESPONSECODE&gt;&lt;TRANSID&gt;scb190116000206&lt;/TRANSID&gt;&lt;REFTRANSID&gt;scb190116000202&lt;/REFTRANSID&gt;&lt;TRANSTYPE&gt;01&lt;/TRANSTYPE&gt;&lt;DATETIME&gt;20190116132014&lt;/DATETIME&gt;&lt;DESCRIPTION&gt;&lt;/DESCRIPTION&gt;&lt;PROVIDERID&gt;AIRPAY&lt;/PROVIDERID&gt;&lt;MAC&gt;62107e95fb7d1994d2af084b968e7abd&lt;/MAC&gt;&lt;/RESPONSE&gt;')

        def listing_notification(assets, quote_asset='BTC'):
            url = 'https://api.binance.com/api/v1/exchangeInfo'
            while True:
                found = []
                reply = requests.get(url)
                symbols = json_helpers.safe_loads(reply.text)['symbols']
                for s in symbols:
                    if s['quoteAsset'] == quote_asset and s['baseAsset'] in assets:
                        print(s['symbol'], s['status'])
                        os.system('/usr/bin/canberra-gtk-play --id=\'phone-outgoing-calling\' --volume=10.0')
                        found.append(s['baseAsset'])
                        if len(found) == len(assets):
                            return
                sleep(1)

        # listing_notification(['VOISE'])

        # print(CardNoUtils.encrypt('123412312311'))
        # print(CardNoUtils.decrypt('YRWQ/a4qbYvsq5X1lBSCEQ=='))
        # print(CardNoUtils.decrypt('v0KpTEn2Tb/0yao07A325Q=='))
        # print(CardNoUtils.decrypt('rghUWjkiDDAuXyjGZbznUg=='))

        def subtract(str1, str2):
            def trim(s):
                while s[0] == '0':
                    s = s[1:]
                return s

            def compare(s1, s2):
                if s1 == s2:
                    return 0
                if len(s1) > len(s2):
                    return 1
                if len(s1) < len(s2):
                    return -1
                if s1 > s2:
                    return 1
                else:
                    return -1

            def _subtract(s1, s2):
                result = ''
                carry = 0
                diff = len(s1) - len(s2)
                for i in range(len(s1) - 1, -1, -1):
                    x = int(s1[i])
                    y = int(s2[i - diff]) if i >= diff else 0
                    if x >= y + carry:
                        result = str(x - y - carry) + result
                        carry = 0
                    else:
                        result = str(x - y - carry + 10) + result
                        carry = 1

                return trim(result)

            str1 = trim(str1)
            str2 = trim(str2)
            cmp = compare(str1, str2)
            if cmp == 0:
                return '0'
            elif cmp > 0:
                return _subtract(str1, str2)
            else:
                return '-' + _subtract(str2, str1)

        # print(subtract('10000', '99'))
        # print(subtract('99', '10000'))
        # print(subtract('123456789', '987654321'))

        class Node(object):
            def __init__(self, value, left=None, right=None):
                self.value = value
                self.left = left
                self.right = right

        def dfs(node):
            """
            Traverse through a tree using DFS strategy starting from the provided node
            :param node: starting node
            :return: list of traversed values
            """
            result = []
            tmp = Node
            return result

        # print(dfs(Node(1, Node(2, Node(3, Node(4), Node(5)), Node(6)), Node(7))))

        def encryption():
            pub_str = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw1juJvCyssSI1jinrdFg
wcKmlLOpm3EEc5R4l6WGHV8phsmM55o40W4kL26impjnxPZM6toaEzd2fGghiEAz
AAaVdyCnxt0peAkDsag891FRToG767969c9fjm0vgKhFPd0MLkDN+RRRhWLYyzmi
PwcAeqoNX3F5YV1sI7jURUOHl8A2IV8bEKLMmrdhx/ITKNEMwS7NfOxSDfrFEl1E
Y9f9hYzHk1vjr4xQi6NIw76gwWv80IXe0fAcdNgXhNtD8M3S44hO630+tnHgDxim
hD9/EJRckFVvqjsVlw8g1zrsv7/zOBlVws/QCFfLZYe4SHAdhsQu85U3rSHhlr/P
BQIDAQAB
-----END PUBLIC KEY-----'''
            pri_str = '''-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAw1juJvCyssSI1jinrdFgwcKmlLOpm3EEc5R4l6WGHV8phsmM
55o40W4kL26impjnxPZM6toaEzd2fGghiEAzAAaVdyCnxt0peAkDsag891FRToG7
67969c9fjm0vgKhFPd0MLkDN+RRRhWLYyzmiPwcAeqoNX3F5YV1sI7jURUOHl8A2
IV8bEKLMmrdhx/ITKNEMwS7NfOxSDfrFEl1EY9f9hYzHk1vjr4xQi6NIw76gwWv8
0IXe0fAcdNgXhNtD8M3S44hO630+tnHgDximhD9/EJRckFVvqjsVlw8g1zrsv7/z
OBlVws/QCFfLZYe4SHAdhsQu85U3rSHhlr/PBQIDAQABAoIBAF6D/65NlViTaNWl
UdPy00rMgEbAatavpwS5GGPfDXXWnkP97rP8VXNXRCDC+d+tDa6psOuMnUMg+a4V
v+upjEN97AFYhnTcevz995CUovLSoHFIqgDVg4u9SzGhOHOadu4IrqUOa9oQ76SG
//fMKeku3Rd8gb3lLGJkjjb2bZYYzaCFMIIVBe5yBUALb7sVmlhmZLnPHG40Tv16
OUGOWO5AXoo6Tg4MV26JmCpkVbRc1QMXwZ4JHMcIlYZSb6OZnW/kXqR/bxGh01DW
p7Jjdxx86pwSzO51G3Zs6jOeNRH2rUUcb1BWhuHfYwqFcApedP3UazbkWxLMpu5M
Fn56pkECgYEA+b8D93CRqGNRsmelio+IiYHnzVsNGG5mGPuXZ2flvHWW9mImJ9E0
lKNpEZGYPmvwIeoF1HhZD8P8GYGQzziNYIrmNzHJ+T9GDl1s76j45oIjBOsotPlY
xjo3cRpadQZsNp7wSMtA1NS6VbjqdSJcr9gN9e2YeU+X8Hp1JqrQo7UCgYEAyD0x
wNT5qGsAjFlZKcAuI1qL+XURnXB/UY9rYHoqt3AavMLaJPFW5+DQxTarotP802cq
DafH9xsFZ71XG0vqKDQmWbgrWG7sTN2iLDC3kQ26iafBJN76MSnejFXSJEL3tuWY
Vc0rw1Sle+jXprk+8noby2Op4ZU7vow1cnVHMBECgYB2D7OLVH628ISdZtvd3a54
+p0e+ez94KqJIt5W9smmxpvfy1QoPICzx3AS6xXiZFo3Xg71exL3HfneAN745s4G
loLwEqxdFGlEvyuRO/q11U1CtPwgWUN7Kegtonyil6+uPoJulw8Fza5seab0SpMw
WV14JaKPrm2wM+OPrO5GhQKBgBF5PZk9PJgU1lRpC53YFm6hXSukqqfZhFLCuDUQ
FCAz2TF1s4GbyeCsPqunDK1F4H82NnZAmPOYWQ1neW15X3KoslwL9URfUaGXiapf
ifVPhGK0z+b+ykh2BeSrLI5bhbBhMrzyDYqbHWHFvOPgsHyKaViDVvTHiBIlvBhD
4bVxAoGALB3msOyNRxLJblFmPrjwamoGp6vWjoh2mc2JfPO/IbF3rrHXtGIS6BW4
wshJJkGKv7Rxy+OimlvvXT7/2a1/awZWLB7ovQlsWz+Viz+fo5Nac/HVSmgJjS6s
uS0D+cB0pfWqccBq2L73ZIR99bQ1jimWgHLzl0XJZS3egG0urs0=
-----END RSA PRIVATE KEY-----'''
            from Crypto import Random
            from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
            from Crypto.Cipher import PKCS1_OAEP

            data = '9704289994066032'

            rsa_pub_key = RSA.importKey(pub_str)
            # h = SHA.new(data)
            encrypter = Cipher_PKCS1_v1_5.new(rsa_pub_key)
            # encrypter = PKCS1_OAEP.new(rsa_pub_key)
            # encrypted_str = base64.b64encode(encrypter.encrypt(data + h.digest()))
            encrypted_str = base64.b64encode(encrypter.encrypt(data))
            print(encrypted_str)
            # encrypted_str = 'L/WwJ74J/5KrZlAW+aNM20XYY1ZSDhFfDyb54t6FEL1AzpMS39EWt4DxS9vVJ2NH+F06qDR95qCI2zT8pNtRsui0bKX68eGMseqfKwTg30di78Qt/3QXue7rncqtguvD/Fxov8iKGguUGMzzK+vp9myP+9vmGuIjjuwNWFRbOwauXITP7T8Cub0KuKPxnLb/0xtvQL+wXPaGJLgNvalya+MeBIutXUmg1/tGIUmf+ckkNIr8a0pp4qy57UM9iSNBsn/ZtXR/PjvEi1axGEpVfbHMWK2VhYvefFAor/uEqFO1fHFs+iAEwOaIxL6Y02Pyf4+Am0GMLrwVhVPbvWy9IOIsQ76R0H2E5ZcAlNrD'
            # encrypted_str = 'CE8UPkwcYoKVrU9iV2daE1MNBV1edcfogCvcvZoVBop8J6Sg5YLGW+dRU5cfAU/7nf/KA3UQBsmznnvhWz6ePVfuei9btcyXQ9/8IbJBW8o0UpUQuxWjC9/BJhCd6hVUmuJOb2vwe7Em1rNSiYRaiteoKs/hRKWwde/4j2V5wTFgM15POfEiVEW1I87ygAlBU5WtuZWXqbkblTNZao4Qz7y2TlNTA3yrzHfc0YxrWfLH3/L+3yxIlQuY361WRdLPQb3AfIUpGPk+uBlpdLEVanQMYcJaRPZ9Aue47zR/JmSVbeyvfZvNPylsgbjNnsZiW/VHCf/Ava5cyb25PdszkDq7UgBApWGpXeEBJEtD'
            # encrypted_str = 'mCKe11DPcvCjXOJ6a/r1tnohOfZFxGzh4iWXATpWhbz6AH4h9YDivjdnZ1Bd+Y7ms9RHZJheftvVFTwE8IrUlxgFxzexMs/QmJxAFQUuMdbwHtTOhw+fjzHMquHGqY/guaISp+b8HzGmlQ2JC7okYhLPI3KG8VLUuEysMs4qmCy+ceGslzN/tFBzif+LhaMbOgx4AUUhoZH1Rfrzjir9J7Uctl7QBLmS/rV+9SoJLwahzdpWn5q8XdZK0kilAVHaezREU+g6IaUKekbLbaBDuv2L6E4UADg0Dcf3oTMR4I9+5ip+Mwx1SucYVIUflkeoa7qZ6483zlJ4Z8s7sSMjRA=='
            rsa_pri_key = RSA.importKey(pri_str)
            decrypter = Cipher_PKCS1_v1_5.new(rsa_pri_key)
            # decrypter = PKCS1_OAEP.new(rsa_pri_key)
            sentinel = Random.new().read(16 + SHA.digest_size)
            decrypted_str = decrypter.decrypt(base64.b64decode(encrypted_str), sentinel)
            # message = decrypter.decrypt(base64.b64decode(encrypted_str), sentinel)
            # decrypted_str = decrypter.decrypt(base64.b64decode(encrypted_str))
            # decrypted_str = message[:-SHA.digest_size]
            # print message[-SHA.digest_size:] == SHA.new(decrypted_str).digest()
            print(decrypted_str)

        # encryption()

        def signature():
            pub_str = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw1juJvCyssSI1jinrdFg
wcKmlLOpm3EEc5R4l6WGHV8phsmM55o40W4kL26impjnxPZM6toaEzd2fGghiEAz
AAaVdyCnxt0peAkDsag891FRToG767969c9fjm0vgKhFPd0MLkDN+RRRhWLYyzmi
PwcAeqoNX3F5YV1sI7jURUOHl8A2IV8bEKLMmrdhx/ITKNEMwS7NfOxSDfrFEl1E
Y9f9hYzHk1vjr4xQi6NIw76gwWv80IXe0fAcdNgXhNtD8M3S44hO630+tnHgDxim
hD9/EJRckFVvqjsVlw8g1zrsv7/zOBlVws/QCFfLZYe4SHAdhsQu85U3rSHhlr/P
BQIDAQAB
-----END PUBLIC KEY-----'''
            pri_str = '''-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAw1juJvCyssSI1jinrdFgwcKmlLOpm3EEc5R4l6WGHV8phsmM
55o40W4kL26impjnxPZM6toaEzd2fGghiEAzAAaVdyCnxt0peAkDsag891FRToG7
67969c9fjm0vgKhFPd0MLkDN+RRRhWLYyzmiPwcAeqoNX3F5YV1sI7jURUOHl8A2
IV8bEKLMmrdhx/ITKNEMwS7NfOxSDfrFEl1EY9f9hYzHk1vjr4xQi6NIw76gwWv8
0IXe0fAcdNgXhNtD8M3S44hO630+tnHgDximhD9/EJRckFVvqjsVlw8g1zrsv7/z
OBlVws/QCFfLZYe4SHAdhsQu85U3rSHhlr/PBQIDAQABAoIBAF6D/65NlViTaNWl
UdPy00rMgEbAatavpwS5GGPfDXXWnkP97rP8VXNXRCDC+d+tDa6psOuMnUMg+a4V
v+upjEN97AFYhnTcevz995CUovLSoHFIqgDVg4u9SzGhOHOadu4IrqUOa9oQ76SG
//fMKeku3Rd8gb3lLGJkjjb2bZYYzaCFMIIVBe5yBUALb7sVmlhmZLnPHG40Tv16
OUGOWO5AXoo6Tg4MV26JmCpkVbRc1QMXwZ4JHMcIlYZSb6OZnW/kXqR/bxGh01DW
p7Jjdxx86pwSzO51G3Zs6jOeNRH2rUUcb1BWhuHfYwqFcApedP3UazbkWxLMpu5M
Fn56pkECgYEA+b8D93CRqGNRsmelio+IiYHnzVsNGG5mGPuXZ2flvHWW9mImJ9E0
lKNpEZGYPmvwIeoF1HhZD8P8GYGQzziNYIrmNzHJ+T9GDl1s76j45oIjBOsotPlY
xjo3cRpadQZsNp7wSMtA1NS6VbjqdSJcr9gN9e2YeU+X8Hp1JqrQo7UCgYEAyD0x
wNT5qGsAjFlZKcAuI1qL+XURnXB/UY9rYHoqt3AavMLaJPFW5+DQxTarotP802cq
DafH9xsFZ71XG0vqKDQmWbgrWG7sTN2iLDC3kQ26iafBJN76MSnejFXSJEL3tuWY
Vc0rw1Sle+jXprk+8noby2Op4ZU7vow1cnVHMBECgYB2D7OLVH628ISdZtvd3a54
+p0e+ez94KqJIt5W9smmxpvfy1QoPICzx3AS6xXiZFo3Xg71exL3HfneAN745s4G
loLwEqxdFGlEvyuRO/q11U1CtPwgWUN7Kegtonyil6+uPoJulw8Fza5seab0SpMw
WV14JaKPrm2wM+OPrO5GhQKBgBF5PZk9PJgU1lRpC53YFm6hXSukqqfZhFLCuDUQ
FCAz2TF1s4GbyeCsPqunDK1F4H82NnZAmPOYWQ1neW15X3KoslwL9URfUaGXiapf
ifVPhGK0z+b+ykh2BeSrLI5bhbBhMrzyDYqbHWHFvOPgsHyKaViDVvTHiBIlvBhD
4bVxAoGALB3msOyNRxLJblFmPrjwamoGp6vWjoh2mc2JfPO/IbF3rrHXtGIS6BW4
wshJJkGKv7Rxy+OimlvvXT7/2a1/awZWLB7ovQlsWz+Viz+fo5Nac/HVSmgJjS6s
uS0D+cB0pfWqccBq2L73ZIR99bQ1jimWgHLzl0XJZS3egG0urs0=
-----END RSA PRIVATE KEY-----'''
            from Crypto.Signature import PKCS1_v1_5 as Signature_PKCS1_v1_5

            rsa_pri_key = RSA.importKey(pri_str)
            sig_maker = Signature_PKCS1_v1_5.new(rsa_pri_key)
            h = SHA.new('9704289994066032')
            sign = sig_maker.sign(h)
            print(base64.b16encode(sign))
            sign = base64.b64encode(sign)
            print (sign)

            rsa_pub_key = RSA.importKey(pub_str)
            verifier = Signature_PKCS1_v1_5.new(rsa_pub_key)
            h = SHA.new('9704289994066032')
            print(verifier.verify(h, base64.b64decode(sign)))

        # print re.match(r'2017-11-09 07:00:54.*tpbank_provider_connector.*', '2017-11-09 07:00:54.320000 | INFO | 30113 : 140025557577072 | tpbank_provider_connector.py: 83 | tpbank_provider_connector. send_request | code: QUERY | request_xml: <?xml version="1.0" encoding="UTF-8" ?><EBG><QUERY_REQ><INFO>1711091600030982</INFO><XREF>1711091600030982</XREF><DESCRIPTION>Check transaction 1711071300000506</DESCRIPTION><ADD_INFO><PRM5></PRM5><PRM4></PRM4><PRM1></PRM1><PRM3></PRM3><PRM2></PRM2></ADD_INFO><TRANS_DATE>20171109070054</TRANS_DATE><SIGNATURE>MB+RkRCIj+jZh8YmkSU5KrpopeQFdO4Fhdb8zDJM0BPC2N0HbOji30H58+Z/Wh7NODnf8LMMORfvPvOsbwMPcV9iaD3RniCQ/osUmSHXFM79U8bjqt44c4t/UPU3TEtsM1/O9b3/lQDJ7f0n1CRX/00WJ9uOwLAraSCa8pNBX3rNRbbBHvESc+jiCnmbxJbVt9CfYdOCV6WHHZThuGdvfqlkJxgC6wiLul4+mvgCoAxbA7X9dsZBovu4UftGs4/mXQ7Brg762R3c9E3iwhmIk3Tkd2aDSFwm0s3Y/rSYNk5HC7+b4Zqezs9MTgzNK94rTsGr4a1pl7XVgh/qQbpo9g==</SIGNATURE><ID>1711071300000506</ID><FN_CODE>QR_TRAN</FN_CODE></QUERY_REQ></EBG>')
        # signature()

        def test_sacombank_ssl():
            reply = requests.get('https://card.sacombank.com.vn/', verify='/home/tuandat/Desktop/card.sacombank.com.vn.crt')
            print(reply.content)

        # test_sacombank_ssl()

        class BinaryReader(object):
            def __init__(self, s):
                self._s = StringIO(s)

            def read_bytes(self, length):
                return self._s.read(length)

            def unpack(self, fmt, length=1):
                return struct.unpack(fmt, self.read_bytes(length))[0]

            def read_char(self):
                return self.unpack('c', 1)

            def read_byte(self):
                return self.unpack('b', 1)

            def read_ubyte(self):
                return self.unpack('B', 1)

            def read_short(self):
                return self.unpack('h', 2)

            def read_ushort(self):
                return self.unpack('H', 2)

            def read_int(self):
                return self.unpack('i', 4)

            def read_uint(self):
                return self.unpack('I', 4)

            def read_long(self):
                return self.unpack('q', 8)

            def read_ulong(self):
                return self.unpack('Q', 8)

            def read_decimal(self):
                return self.unpack('2q', 16)

            def read_string(self):
                # parse length as 7BitEncodedInt
                length = self.read_byte()
                while length == 0:  # ignore padding byte
                    length = self.read_byte()
                index = 0
                signal = (length & 0x80) >> 7
                length = length & 0x7f
                while signal > 0:
                    index += 1
                    byte = self.read_byte()
                    signal = (byte & 0x80) >> 7
                    length |= (byte & 0x7f) << (7 * index)
                return self.unpack('{}s'.format(length), length)

        def parse_home_creadit_binary_data():
            b64 = 'RntJTwIAAAAAAAAAAAAAABNOR1VZ4buETiBTT05HIFTDmU5HCioqKioqKjg2ODUWiwIAAAAAAAAAAAAAAAAAFosCAAAAAAAAAAAAAAAAAAoxMS0wNi0yMDE1IFJldHJpZXZpbmcgZGF0YSBpcyBzdWNjZXNzZnVsbHkuAQAAAAMAAAA='
            br = BinaryReader(base64.b64decode(b64))
            data = object()
            data.contract_number = br.read_decimal()
            data.customer_name = br.read_string()
            data.customer_number = br.read_string()
            data.total_amount = br.read_decimal()
            data.remaining_amount = br.read_decimal()
            data.date = br.read_string()
            data.description = br.read_string()
            data.response_code = br.read_short()
            return data

        # parse_home_creadit_binary_data()

