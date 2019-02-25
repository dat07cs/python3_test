from lxml import etree
import xmlsec


class SignatureOptions(object):
    transform_type = xmlsec.constants.TransformEnveloped
    c14n_method = xmlsec.constants.TransformInclC14N
    sign_method = xmlsec.constants.TransformRsaSha1
    digest_method = xmlsec.constants.TransformSha1


class EncryptionOptions(object):
    session_key = None
    encryption_method = xmlsec.constants.TransformAes256Cbc
    key_encryption_method = xmlsec.constants.TransformRsaPkcs1
    key_data_type = xmlsec.constants.KeyDataAes
    key_size = 256


class XmlSecUtils(object):
    def __init__(self, key_path, cert_path, signature_options=None, encryption_options=None):
        self.key_path = key_path
        self.cert_path = cert_path
        self.signature_options = signature_options or SignatureOptions()
        self.encryption_options = encryption_options or EncryptionOptions()

    def sign(self, node, get_object=False):
        options = self.signature_options

        # load private key in pem format (assuming that there is no password)
        key = xmlsec.Key.from_file(self.key_path, xmlsec.constants.KeyDataFormatPem)
        # load the certificate in pem format and add it to the key
        key.load_cert_from_file(self.cert_path, xmlsec.constants.KeyDataFormatCertPem)

        # create a signature template
        sig_data = xmlsec.template.create(node, c14n_method=options.c14n_method, sign_method=options.sign_method)
        # add the <ds:Signature/> node to the document
        node.append(sig_data)
        # add the <ds:Reference/> node to the signature template.
        ref = xmlsec.template.add_reference(sig_data, digest_method=options.digest_method)
        # add transform descriptor
        xmlsec.template.add_transform(ref, transform=options.transform_type)
        xmlsec.template.add_transform(ref, transform=options.c14n_method)
        # add the <ds:KeyInfo/> and <ds:KeyName/> nodes
        key_info = xmlsec.template.ensure_key_info(sig_data)
        x509_data = xmlsec.template.add_x509_data(key_info)
        x509_issuer_serial = xmlsec.template.x509_data_add_issuer_serial(x509_data)
        xmlsec.template.x509_issuer_serial_add_issuer_name(x509_issuer_serial)
        xmlsec.template.x509_issuer_serial_add_serial_number(x509_issuer_serial)

        # create a digital signature context (no key manager is needed)
        sig_ctx = xmlsec.SignatureContext()
        sig_ctx.key = key

        # sign using signature template
        sig_ctx.sign(sig_data)

        if get_object is True:
            return node

        return etree.tostring(node)

    def verify(self, signed_data):
        # load the certificate in pem format
        cert = xmlsec.Key.from_file(self.cert_path, xmlsec.constants.KeyDataFormatCertPem)

        # find the <Signature/> node.
        signature_node = xmlsec.tree.find_node(signed_data, xmlsec.constants.NodeSignature)

        # create a digital signature context (no key manager is needed)
        sig_ctx = xmlsec.SignatureContext()
        sig_ctx.key = cert

        # verify the signature.
        try:
            sig_ctx.verify(signature_node)
        except xmlsec.VerificationError:
            return False

        return True

    def encrypt(self, node, get_object=False):
        options = self.encryption_options

        # load the certificate in pem format
        cert = xmlsec.Key.from_file(self.cert_path, xmlsec.constants.KeyDataFormatCertPem)

        # create key manager
        manager = xmlsec.KeysManager()
        manager.add_key(cert)

        # create a encryption context
        enc_ctx = xmlsec.EncryptionContext(manager=manager)
        enc_ctx.key = xmlsec.Key.generate(options.key_data_type, options.key_size, xmlsec.constants.KeyDataTypeSession)

        # create encrypted data template
        enc_data = xmlsec.template.encrypted_data_create(
            node, method=options.encryption_method, type=xmlsec.constants.TypeEncElement)
        # ensure cipher value
        xmlsec.template.encrypted_data_ensure_cipher_value(enc_data)
        # ensure key info
        key_info = xmlsec.template.encrypted_data_ensure_key_info(enc_data)
        if options.session_key is not None:
            xmlsec.template.add_key_name(key_info, name=options.session_key)
        # add encrypted key
        enc_key = xmlsec.template.add_encrypted_key(key_info, method=options.key_encryption_method)
        # ensure key info's cipher value
        xmlsec.template.encrypted_data_ensure_cipher_value(enc_key)

        enc_data = enc_ctx.encrypt_xml(enc_data, node)

        if get_object is True:
            return enc_data

        return etree.tostring(enc_data)

    def decrypt(self, encrypted_data, get_object=False):
        # load private key in pem format (assuming that there is no password)
        key = xmlsec.Key.from_file(self.key_path, xmlsec.constants.KeyDataFormatPem)

        # create key manager
        manager = xmlsec.KeysManager()
        manager.add_key(key)

        # create encryption context
        enc_ctx = xmlsec.EncryptionContext(manager=manager)

        decrypted_data = enc_ctx.decrypt(encrypted_data)

        if get_object is True:
            return decrypted_data

        return etree.tostring(decrypted_data)

    def sign_and_encrypt(self, node, get_object=False):
        signed_node = self.sign(node, get_object=True)
        return self.encrypt(signed_node, get_object=get_object)

    def decrypt_and_verify(self, encrypted_data, remove_signature_node=True, get_object=False):
        decrypted_data = self.decrypt(encrypted_data, get_object=True)
        if self.verify(decrypted_data):
            if remove_signature_node is True:
                # remove the <Signature/> node.
                signature_node = xmlsec.tree.find_node(decrypted_data, xmlsec.constants.NodeSignature)
                decrypted_data.remove(signature_node)
            if get_object is True:
                return decrypted_data
            return etree.tostring(decrypted_data)
        return None

    def _find_child(self, node, name, namespace):
        return xmlsec.tree.find_child(node, name, namespace)


if __name__ == '__main__':
    _node = etree.parse('/workspace/personal/python_test/files/enc1-doc.xml').getroot()
    _key_path = '/workspace/personal/python_test/keys/myKey.pem'
    _cert_path = '/workspace/personal/python_test/keys/myCert.pem'

    xmlsec_utils = XmlSecUtils(key_path=_key_path, cert_path=_cert_path, signature_options=SignatureOptions(),
                               encryption_options=EncryptionOptions())

    _signed_node = xmlsec_utils.sign(_node)
    assert xmlsec.tree.find_node(etree.fromstring(_signed_node.decode()), xmlsec.constants.NodeSignature) is not None
    with open('/workspace/personal/python_test/files/enc1-res.xml', 'wb') as fh:
        fh.write(_signed_node)

    _encrypted_data = xmlsec_utils.encrypt(etree.fromstring(_signed_node))
    with open('/workspace/personal/python_test/files/enc1-encrypted.xml', 'wb') as fh:
        fh.write(_encrypted_data)

    _decrypted_data = xmlsec_utils.decrypt(etree.fromstring(_encrypted_data))
    assert _signed_node == _decrypted_data

    _verified = xmlsec_utils.verify(etree.fromstring(_decrypted_data.decode()))
    assert _verified is True

    _node = etree.parse('/workspace/personal/python_test/files/enc1-doc.xml').getroot()
    _encrypted_data = xmlsec_utils.sign_and_encrypt(_node, get_object=True)
    _decrypted_data = xmlsec_utils.decrypt_and_verify(_encrypted_data, get_object=False)
    with open('/workspace/personal/python_test/files/enc1-doc.xml', 'rb') as _fh:
        _raw_data = _fh.read()
    assert _decrypted_data == _raw_data
    print(_decrypted_data.decode())
