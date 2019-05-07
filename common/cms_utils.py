from M2Crypto import BIO, SMIME, X509


def encrypt(data, cert_path='/workspace/personal/python_test/keys/myCert.pem', compact=True):
    # Make a MemoryBuffer of the message.
    buf = BIO.MemoryBuffer(data)

    # Instantiate an SMIME object.
    s = SMIME.SMIME()

    # Load target cert to encrypt to.
    x509 = X509.load_cert(cert_path)
    sk = X509.X509_Stack()
    sk.push(x509)
    s.set_x509_stack(sk)

    # Set cipher: 3-key triple-DES in CBC mode.
    s.set_cipher(SMIME.Cipher('des_ede3_cbc'))

    # Encrypt the buffer.
    p7 = s.encrypt(buf)

    # Output p7 to a MemoryBuffer.
    out = BIO.MemoryBuffer()
    s.write(out, p7)

    # Read output as string
    output = out.read()
    if compact:
        # create a single line encrypted message
        output = ''.join(output.split('\n')[5:])

    return output


def decrypt(key_path='/workspace/personal/python_test/keys/myKey.pem',
            cert_path='/workspace/personal/python_test/keys/myCert.pem'):
    # Instantiate an SMIME object.
    s = SMIME.SMIME()
    # Load private key and cert.
    s.load_key(key_path, cert_path)
    # Load the encrypted data.
    encrypted_data = """MIME-Version: 1.0
Content-Disposition: attachment; filename="smime.p7m"
Content-Type: application/pkcs7-mime; smime-type=enveloped-data; name="smime.p7m"
Content-Transfer-Encoding: base64

MIIC/AYJKoZIhvcNAQcDoIIC7TCCAukCAQAxggKlMIICoQIBADCBiDB7MQswCQYD
VQQGEwJWTjEMMAoGA1UECAwDSENNMQwwCgYDVQQHDANIQ00xDDAKBgNVBAoMA1NF
QTEMMAoGA1UECwwDQ09EMQ8wDQYDVQQDDAZBaXJQYXkxIzAhBgkqhkiG9w0BCQEW
FGFpcnBheV92bkB2ZWQuY29tLnZuAgkAvMiAJGI+ZHswDQYJKoZIhvcNAQEBBQAE
ggIAF8Wx6U5Sf2VXEBkfm8uhPey5tRJeCBLrWmjpkSCq7sm0vZV3CpRaT1LPYyjF
ugS1EEAb36MPDZkTAg1NniyLMfVjoio2gUWlrBmdIiB6O8ElaHWYbqmsiFrhszGx
XHDCTAQB6pXGqVE5lhjIBD92wqJSwmxlSwD0m4KG5JNv92fDvm3G5CgEGAjUYsWf
Y1E2BJUoCDHUsD+4IKItlLJzHMMQc3e2SyGTlSjrayAVZsUbYRfunhr4o9uKsKM6
28h4Hs1I6ekZ1O2COCvM4k/Tv3o+rbLBXdRy27POOI2ksrY0ub96aw9Ks2QZTYoV
c4iNCGEXVHr7PRwBgeDZKBH1xM929gsVcQOVCy5IaEUvSrlhg/VSMiOis3rYv1p+
R0Frd4Ep8RdaPMStUNDSU4Ia1FCzTpiWCNfPj9940U3vMoPu1l+q2WBbOPmrknaC
pI6hqvFYGBVx4i0zfatoycs1S6p4EPKoe/XAe0Rosi94RKE8H6gQurmhYcKT+zwF
boRGPnKs1rxVn2sHJ3KYmCGfgoWUmOzEHpmTelIt/lXHiPd4cIT42tvT1OLne0aU
/Qvo1K1KffiEGC+hbHEG5Y/lH/9QYsYp7KiGyYdYj7QOnBv9d0taDXscYbdpTv8z
Kbb39iPDQ07F6/MQ1C5GkIK6azMa+YKdMK4grtTHVXaPrLEwOwYJKoZIhvcNAQcB
MBQGCCqGSIb3DQMHBAjBmOK7gvkV3oAYjNbjiFIv1Iu4gF+uSKW+zzQrU0Jiabgg
"""
    data = BIO.MemoryBuffer(encrypted_data.encode())
    p7, data = SMIME.smime_load_pkcs7_bio(data)
    # p7, data = SMIME.smime_load_pkcs7('/workspace/personal/python_test/keys/encrypt.txt')
    # Decrypt p7.
    out = s.decrypt(p7)
    return out


if __name__ == '__main__':
    # print encrypt(data='test text data')
    print(decrypt())
