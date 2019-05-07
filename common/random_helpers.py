import datetime
import random
import string


def rand_key(length: int = 16, allowed_characters: str = None) -> str:
    if allowed_characters is None:
        allowed_characters = string.ascii_letters + string.digits + '~!@#$%^&*()_-+='
    return ''.join(random.choice(allowed_characters) for _ in range(length))


def rand_id(precision: int = 4) -> str:
    res = datetime.datetime.now().strftime('%s')
    if precision > 0:
        res += str(random.randint(0, pow(10, precision) - 1))
    return res
