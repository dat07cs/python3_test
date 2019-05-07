import inspect
import unittest
from importlib import import_module

from typing import Type

from services import service_base
from services.service_base import BaseService, ClientBaseService, ProviderBaseService
from tests.testcase import SimpleTestCase


class ServiceBaseTestCase(SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        super(ServiceBaseTestCase, cls).setUpClass()
        cls.service_manager = service_base.ServiceManager()
        cls.service_manager.load_service_map()
        cls.client_services = cls.service_manager.client_services
        cls.provider_services = cls.service_manager.provider_services

    def ensure_client_service(self, bank_id, *service_names):
        for service_name in service_names:
            service = self.client_services.get((bank_id, service_name))
            self.assertIsNotNone(service, 'Service not registered bank=%s, name=%s' % (bank_id, service_name))
            try:
                service()
            except Exception as exc:
                self.fail('Failed to instantiate class %s, exception: %s' % (service.__name__, str(exc)))

    def ensure_provider_service(self, bank_id, *service_names):
        for service_name in service_names:
            service = self.provider_services.get((bank_id, service_name))
            self.assertIsNotNone(service, 'Service not registered bank=%s, name=%s' % (bank_id, service_name))
            try:
                service()
            except Exception as exc:
                self.fail('Failed to instantiate class %s, exception: %s' % (service.__name__, str(exc)))

    def test_auto_discover(self):
        def test_module(m):
            predicate = lambda x: inspect.isclass(x) and issubclass(x, BaseService) and x.__module__ == m.__name__
            service_classes = (service_class for _, service_class in inspect.getmembers(m, predicate))
            for service_class in service_classes:  # type: Type[BaseService]
                try:
                    if issubclass(service_class, (ClientBaseService, ProviderBaseService)):
                        service_class()
                except Exception as exc:
                    self.fail('Failed to instantiate class %s, exception: %s' % (service_class.__name__, str(exc)))

        for _, name in ():  # fixme
            m = import_module('services.%s_services' % name.lower())
            test_module(m)


if __name__ == '__main__':
    unittest.main()
