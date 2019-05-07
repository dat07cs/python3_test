import string

from common import logger


def lpad(orig, char, length):
    """
    Pad more character to the left of original string to have enough length.
    If original string length is longer than expected string, there is no change
    :param orig: original string
    :param char: filling character
    :param length: expected length of result string
    :return: Padded string or original string
    """
    orig = str(orig)
    src_len = len(orig)
    missing_len = length - src_len
    if missing_len > 0:
        orig = '{}{}'.format((missing_len * char), orig)
    return orig


def rpad(orig, char, length):
    """
    Pad more character to the right of original string to have enough length.
    If original string length is longer than expected string, there is no change
    :param orig: original string
    :param char: filling character
    :param length: expected length of result string
    :return: Padded string or original string
    """
    orig = str(orig)
    src_len = len(orig)
    missing_len = length - src_len
    if missing_len > 0:
        orig = '{}{}'.format(orig, (missing_len * char))
    return orig


VIETNAMESE_TRANSLATE_TABLE = None


def normalize_vietnamese(text, unicode_escape=False):
    if text and isinstance(text, (str, bytes)):
        _ensure_vietnamese_translate_table()
        if isinstance(text, str):
            text = text.encode('utf-8')
        if unicode_escape is True:
            try:
                text = text.decode('unicode_escape')
            except:
                logger.main.warning('failed to escape unicode characters %s' % text)
                text = text.decode()
        text = text.translate(VIETNAMESE_TRANSLATE_TABLE)
        text = filter(lambda x: x in string.printable, text)
    return text


def _ensure_vietnamese_translate_table():
    global VIETNAMESE_TRANSLATE_TABLE
    if VIETNAMESE_TRANSLATE_TABLE is None:
        to_replace = 'áàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ'
        to_replace += to_replace.upper()
        replace_to = 'aaaaaaaaaaaaaaaaadeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyy'
        replace_to += replace_to.upper()
        VIETNAMESE_TRANSLATE_TABLE = dict((ord(to_replace[i]), replace_to[i]) for i in range(len(to_replace)))
