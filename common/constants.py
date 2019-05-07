from enum import Enum


class ChoiceEnum(Enum):
    @property
    def display_string(self):
        return ' '.join(x.capitalize() for x in self.name.split('_'))

    @classmethod
    def value_list(cls):
        # noinspection PyTypeChecker
        return list(map(lambda x: x.value, cls))

    @classmethod
    def get_choices(cls, all_choice=('', '--All--')):
        # noinspection PyTypeChecker
        choices = [(x.value, x.display_string) for x in cls]
        if all_choice:
            choices = [all_choice] + choices
        return choices


class FileType(str, ChoiceEnum):
    CSV = 'CSV'
    XLSX = 'XLSX'


class ContentType(str, Enum):
    PLAIN_TEXT = 'text/plain'
    JSON = 'application/json'
    XML_TEXT = 'application/xml'
    HTTP_RESPONSE = 'HttpResponse'


class GiroOTPType(Enum):
    OPTIONAL = 0  # based on reply error code
    MANDATORY = 1  # always required
    NONE = 2  # no otp


class HttpStatus(int, Enum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    INTERNAL_SERVER_ERROR = 500
