from lxml import etree
from signxml import XMLSigner, XMLVerifier, methods
from signxml.exceptions import InvalidSignature


def sign(node, key_path, cert_path, get_object=False):
    key = import_key(key_path)
    cert = import_key(cert_path)
    signer = XMLSigner(method=methods.enveloped, signature_algorithm='rsa-sha1', digest_algorithm='sha1',
                       c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315')
    signed_node = signer.sign(node, key=key, cert=cert)
    if get_object is True:
        return signed_node
    return etree.tostring(signed_node)


def import_key(key_path):
    with open(key_path, 'rb') as fh:
        key = fh.read()
    return key


def verify(signed_data, cert_path):
    cert = import_key(cert_path)
    verifier = XMLVerifier()
    try:
        # noinspection PyTypeChecker
        result = verifier.verify(signed_data, x509_cert=cert)
    except InvalidSignature as exc:
        raise Exception('signature verification failed', exc)
    return result.signed_data


if __name__ == '__main__':
    _data = etree.parse('/workspace/personal/python_test/files/enc1-doc.xml').getroot()
    _key_path = '/workspace/personal/python_test/keys/myKey.pem'
    _cert_path = '/workspace/personal/python_test/keys/myCert.pem'

    _signed_data = sign(_data, key_path=_key_path, cert_path=_cert_path)
    with open('/workspace/personal/python_test/files/enc1-res.xml', 'wb') as _fh:
        _fh.write(_signed_data)
    print(_signed_data.decode())

    _xml_data = verify(_signed_data, cert_path=_cert_path)
    print(_xml_data.decode())
