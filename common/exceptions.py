import json
from typing import Any

from django.http import HttpResponse, JsonResponse
from rest_framework.exceptions import APIException, MethodNotAllowed
from rest_framework.views import exception_handler


class BaseAPIException(APIException):
    status_code = 200

    def __init__(self, response_code: int = 500, detail: Any = None):
        self.error_code = response_code
        super(BaseAPIException, self).__init__(detail=detail)


def _build_response(response_code, context):
    response = exception_handler(BaseAPIException(response_code), context)
    body = json.dumps({'code': response_code})
    return HttpResponse(content=body, content_type="application/json", status=response.status_code)


def my_exception_handler(exc, context):
    """
    Call REST framework's default exception handler first, to get the standard error response.

    should add this into REST_FRAMEWORK configuration.

    REST_FRAMEWORK = {
        'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
    }
    """
    if isinstance(exc, BaseAPIException):
        response_code = exc.error_code
    elif isinstance(exc, MethodNotAllowed):
        response_code = 403
    else:
        response_code = 500

    response_data = {'code': response_code}
    response = exception_handler(BaseAPIException(response_code), context)

    return JsonResponse(data=response_data, status=response.status_code)
