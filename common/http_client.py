import json

import requests

DEFAULT_TIMEOUT = 30


def http_get(url, params=None, timeout=DEFAULT_TIMEOUT, json_body=False):
    http_resp = requests.get(url, data=params, timeout=timeout, verify=False)
    http_resp.raise_for_status()
    try:
        if json_body:
            response = json.loads(http_resp.text)
        else:
            response = http_resp.text
    except:
        response = None
    return response


def http_post(url, params, timeout=DEFAULT_TIMEOUT, json_body=False):
    http_resp = requests.post(url, data=params, timeout=timeout, verify=False)
    http_resp.raise_for_status()
    try:
        if json_body:
            response = json.loads(http_resp.text)
        else:
            response = http_resp.text
    except:
        response = None
    return response
