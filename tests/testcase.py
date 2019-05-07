from django.test import testcases


class SimpleTestCase(testcases.SimpleTestCase):
    def __str__(self):
        return "%s.%s.%s" % (self.__module__, self.__class__.__name__, self._testMethodName)


class TransactionTestCase(testcases.TransactionTestCase):
    def __str__(self):
        return "%s.%s.%s" % (self.__module__, self.__class__.__name__, self._testMethodName)
