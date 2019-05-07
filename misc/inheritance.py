class BaseClass(object):
    class_variable = None

    @classmethod
    def class_method_1(cls):
        print('%s=%s(%s)' % ('cls.class_variable', cls.class_variable, hex(id(cls.class_variable))))


class ChildClass1(BaseClass):
    class_variable = object()


class ChildClass2(BaseClass):
    class_variable = object()


ChildClass1().class_method_1()
ChildClass2().class_method_1()
BaseClass().class_method_1()
