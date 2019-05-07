import traceback

from django.conf import settings


def format_exc_info(exc_info):
    if exc_info[0] is None:
        return 'None'
    lines = traceback.format_exception(*exc_info)
    return ''.join(line for line in lines)


def reverse_dict(d):
    return {value: key for (key, value) in d.items()}


def get_current_url(request):
    if settings.USE_SSL:
        return 'https://' + request.get_host()
    else:
        return 'http://' + request.get_host()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def skip_verify_partner_signature():
    return getattr(settings, 'SKIP_PARTNER_SIGNATURE', False) is True


def skip_verify_gateway_signature():
    return getattr(settings, 'SKIP_GATEWAY_SIGNATURE', False) is True


def unreferenced_parameter(*args):
    return args


def dict_to_object(data):
    return None
