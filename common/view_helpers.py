from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from common import json_helpers, signature
from common.exceptions import BaseAPIException
from common.logger import main as logger


class ServiceExit(Exception):
    pass


class BaseAPIView(APIView):
    http_method_names = ['post']

    _reply = None

    SERIALIZER_CLASS = None

    def __init__(self, **kwargs):
        super(BaseAPIView, self).__init__(**kwargs)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        logger.info(
            '[> Begin]. API: %s, method: %s, GET: %s, POST: %s, body: %s',
            self.get_view_name(), request.method, request.GET, request.POST, request.body
        )
        response = super(BaseAPIView, self).dispatch(request, *args, **kwargs)
        logger.info('[< End]. API: %s, response: %s', self.get_view_name(), response.content)
        return response

    def post(self, request, *args, **kwargs):
        validated_data = self._validate_request(request)
        kwargs['request'] = request
        try:
            self.execute_request(validated_data, *args, **kwargs)
        except ServiceExit:
            return self._reply

    def _validate_request(self, request):
        # validators.validate_admin_ip(request)
        serializer = self.SERIALIZER_CLASS(data=request.data)
        if not serializer.is_valid():
            try:
                error_message = str(serializer.errors.values()[0][0])
            except:
                error_message = serializer.errors
            raise BaseAPIException(response_code=400, detail=error_message)
        if not self._is_valid_signature(serializer.validated_data):
            raise BaseAPIException(response_code=401)
        return serializer.validated_data

    def _is_valid_signature(self, validated_data):
        signature_str = validated_data.get('signature')
        if not signature_str:
            return True  # intended by serializer
        if settings.ENVIRONMENT != settings.LIVE_ENV and 'ignored' in signature_str.lower():
            return True
        copied_data = dict(validated_data)
        copied_data.pop('signature')
        signed_str = json_helpers.json_compact_dumps(copied_data)
        return signature.verify(settings.PARTNER_PUBLIC_KEY_PATH, signed_str, signature_str)

    def reply_json(self, **kwargs):
        self._reply = JsonResponse(kwargs)
        raise ServiceExit

    def raise_error(self, response_code, data=None):
        response_data = {'code': response_code, 'data': data}
        return self.reply_json(**response_data)

    def execute_request(self, validated_data, *args, **kwargs):
        pass
