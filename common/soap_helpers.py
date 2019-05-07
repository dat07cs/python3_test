import zeep
from requests import Session
from requests.auth import HTTPBasicAuth
from suds import plugin as suds_plugin
from zeep import plugins as zeep_plugin


class SOAPENVFixerPlugin(suds_plugin.MessagePlugin):
    def received(self, context):
        # noinspection PyUnresolvedReferences
        context.envelope.nsprefixes['SOAP-ENV'] = 'SOAP-ENV'


class BasicAuthSession(Session):
    def __init__(self, wsse_username: str, wsse_password: str):
        super().__init__()
        self.auth = HTTPBasicAuth(wsse_username, wsse_password)


class HistoryZeepClient(zeep.Client):
    history = zeep_plugin.HistoryPlugin()

    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)
        self.plugins.append(self.history)

    def last_sent(self):
        return self.history.last_sent['envelope']

    def last_received(self):
        return self.history.last_received['envelope']
