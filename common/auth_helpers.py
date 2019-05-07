from django.conf import settings
from django.http.response import HttpResponse, HttpResponseRedirect
from access_tokens import scope, tokens
import hashlib
import json
import base64
from common import serializers, request_helpers
from urllib.parse import urlencode

from common.exceptions import BaseAPIException
from common.json_helpers import ExtendedJsonEncoder
from common.utility_helpers import get_current_url


class AuthorizeSerializer(serializers.NonModelSerializer):
    access_token = serializers.CharField(required=False)
    redirect_url = serializers.CharField(required=False)


def authorized(a_view):
    def _wrapped_view(request, *args, **kwargs):
        auth = authorize(request)
        if auth is not None:
            return auth

        return a_view(request, *args, **kwargs)

    return _wrapped_view


def authorize(request):
    request_data = request_helpers.get_request_data(request)
    serializer = AuthorizeSerializer(data=request_data)

    redirect_url = None
    access_token = request.META.get('HTTP_AUTHORIZATION')
    if serializer.is_valid():
        data = serializer.validated_data
        redirect_url = data.get('redirect_url', None)
        if access_token is None:
            access_token = data.get('access_token', None)

    is_valid = False
    if access_token is not None:
        access_token = access_token.replace('Bearer ', '')
        is_valid = verify_access_token(access_token)

    if not is_valid:
        if redirect_url is None:
            return HttpResponse('Unauthorized', status=401)

        query_dict = {'redirect_url': str(redirect_url)}
        invalid_token_url = get_current_url(request) + '/user/verify/invalid_token/'
        invalid_token_url = invalid_token_url + '?' + urlencode(query_dict)
        return HttpResponseRedirect(invalid_token_url)


def verify_access_token(access_token):
    try:
        decode_access_token = base64.b64decode(access_token).decode('utf-8')
        salt = decode_access_token[:32]
        access_token = decode_access_token[32:]
        is_valid = tokens.validate(access_token, scope.access_app("access_tokens", "publish"),
                                   key=settings.SECRET_KEY, salt=salt, max_age=settings.ACCESS_TOKEN_EXPIRE_INTERVAL)
    except:
        is_valid = False
    return is_valid


def generate_access_token(**kwargs):
    try:
        m = hashlib.md5()
        m.update(json.dumps(kwargs, cls=ExtendedJsonEncoder).encode('utf-8'))
        salt = m.hexdigest()
        access_token = tokens.generate(scope.access_app("access_tokens", "publish"), key=settings.SECRET_KEY, salt=salt)
        return base64.b64encode((salt + access_token).encode('ascii')).decode('ascii')
    except:
        raise BaseAPIException()
