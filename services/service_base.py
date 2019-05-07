import abc
from abc import ABCMeta
from typing import Type, Dict, Tuple

import dicttoxml
import xmltodict
from django.http.response import HttpResponse

import services
from common import constants, json_helpers
from common.exceptions import BaseAPIException
from common.logger import main as logger


class BaseService(object):
    __metaclass__ = abc.ABCMeta
    BANK_ID = abc.abstractproperty()  # type: int
    SERVICE_REGISTRY = abc.abstractproperty()  # type: str

    @abc.abstractmethod
    def generate_transaction_id(self, **kwargs):
        """
        :rtype: basestring
        """

    @property
    def classname(self):
        return self.__class__.__name__

    @abc.abstractmethod
    def __call__(self, request_data):
        """
        :type request_data: dict
        :rtype: ServiceResponse
        """


class ClientBaseService(BaseService, metaclass=ABCMeta):
    pass


class ProviderBaseService(BaseService, metaclass=ABCMeta):
    pass


class ServiceResponse(object):
    _data = None

    def __init__(self, content_type, data):
        self._content_type = content_type  # type: constants.ContentType
        if data:
            self.data = data

    @property
    def content_type(self):
        return self._content_type.value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def text(self):
        return self._data if isinstance(self._data, (str, bytes)) else str(self._data)

    @property
    def http_response(self):
        return HttpResponse(self.text, content_type=self.content_type)

    def __str__(self):
        return self.text


class HttpServiceResponse(ServiceResponse):
    def __init__(self, data=None):
        super(HttpServiceResponse, self).__init__(constants.ContentType.HTTP_RESPONSE, data)

    @property
    def content_type(self):
        if self._data:
            return self._data.get('Content-Type') or constants.ContentType.PLAIN_TEXT.value
        return constants.ContentType.PLAIN_TEXT.value

    @property
    def data(self):
        return self.text

    @data.setter
    def data(self, data):
        assert isinstance(data, HttpResponse)
        self._data = data

    @property
    def text(self):
        # noinspection PyUnresolvedReferences
        return self._data.content.decode()


class JsonServiceResponse(ServiceResponse):
    def __init__(self, data=None):
        super(JsonServiceResponse, self).__init__(constants.ContentType.JSON, data)

    @property
    def data(self):
        if isinstance(self._data, (str, bytes)):
            return json_helpers.safe_loads(self._data)
        return self._data

    @data.setter
    def data(self, data):
        assert isinstance(data, (str, bytes, dict))
        if isinstance(data, bytes):
            data = data.decode()
        self._data = data

    @property
    def text(self):
        if isinstance(self._data, dict):
            return json_helpers.json_compact_dumps(self._data)
        return self._data


class XmlServiceResponse(ServiceResponse):
    def __init__(self, data=None, xml_root='root'):
        super(XmlServiceResponse, self).__init__(constants.ContentType.XML_TEXT, data)
        self._xml_root = xml_root

    @property
    def data(self):
        if isinstance(self._data, (str, bytes)):
            return xmltodict.parse(self._data)[self._xml_root]
        return self._data

    @data.setter
    def data(self, data):
        assert isinstance(data, (str, bytes, dict))
        if isinstance(data, bytes):
            try:
                data = data.decode()
            except:
                pass
        self._data = data

    @property
    def text(self):
        if isinstance(self._data, dict):
            return dicttoxml.dicttoxml(self._data, attr_type=False, custom_root=self._xml_root)
        return self._data


class TextServiceResponse(ServiceResponse):
    def __init__(self, data=None):
        super(TextServiceResponse, self).__init__(constants.ContentType.PLAIN_TEXT, data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        assert isinstance(data, (str, bytes, dict))
        if isinstance(data, bytes):
            data = data.decode()
        self._data = data


class ServiceManager(object):
    """
    Auto discover services in the current package.
    A module can be explicitly excluded from auto discovering by setting the "__autodiscover__" attribute to False. 
    """
    def __init__(self):
        self._client_services = {}  # type: Dict[Tuple[int, str], Type[BaseService]]
        self._provider_services = {}  # type: Dict[Tuple[int, str], Type[BaseService]]

    @property
    def client_services(self):
        return self._client_services

    @property
    def provider_services(self):
        return self._provider_services

    def _is_loaded(self):
        return len(self._client_services) > 0 and len(self._provider_services) > 0

    def load_service_map(self, force=False):
        if force is False and self._is_loaded():
            return

        import inspect
        from importlib import import_module

        self._client_services.clear()
        self._provider_services.clear()

        def service_predicate(x):
            return inspect.isclass(x) and not inspect.isabstract(x) and issubclass(x, BaseService)

        modules = (import_module(module) for module in self._walk_valid_service_pyc_modules())
        modules = filter(lambda x: getattr(x, '__autodiscover__', True) is True, modules)
        for m in modules:
            service_classes = (service_class for _, service_class in inspect.getmembers(m, service_predicate))
            for service in service_classes:  # type: Type[BaseService]
                assert service.BANK_ID is not None, service
                assert service.SERVICE_REGISTRY is not None, service
                if issubclass(service, ClientBaseService):
                    self._client_services[service.BANK_ID, service.SERVICE_REGISTRY] = service
                elif issubclass(service, ProviderBaseService):
                    self._provider_services[service.BANK_ID, service.SERVICE_REGISTRY] = service
                else:
                    logger.warning('cannot register service=%s, bank_id=%s, path=%s.%s',
                                   service.SERVICE_REGISTRY, service.BANK_ID, service.__module__, service.__name__)

    def _walk_valid_service_pyc_modules(self):
        import os
        import pkgutil
        current_path = os.path.dirname(__file__)
        for _, module, ispkg in pkgutil.iter_modules(services.__path__):
            if ispkg is False:
                pyc_file_path = os.path.join(current_path, module + '.pyc')
                if not os.path.isfile(pyc_file_path[:-1]):
                    logger.info('removed invalid pyc file %s' % pyc_file_path)
                    os.remove(pyc_file_path)
                else:
                    yield '%s.%s' % (services.__name__, module)

    def get_client_service(self, bank_id, service_name):
        """
        :rtype: type of ClientBaseService
        """
        return self._get_service(bank_id, service_name, self._client_services)

    def get_provider_service(self, bank_id, service_name):
        """
        :rtype: type of ProviderBaseService
        """
        return self._get_service(bank_id, service_name, self._provider_services)

    def _get_service(self, bank_id, service_name, registered_services):
        self.load_service_map()

        if (bank_id, service_name) not in registered_services:
            raise BaseAPIException(response_code=404, detail='service=%s, bank_id=%s' % (service_name, bank_id))
        return registered_services[bank_id, service_name]


_manager = ServiceManager()


def get_service(bank_id, service_name):
    return _manager.get_client_service(bank_id, service_name)


def get_provider_service(bank_id, service_name):
    return _manager.get_provider_service(bank_id, service_name)
