from urllib import parse


def build_url(url, query_params=None, clear_none=False):
    if query_params is None:
        query_params = {}
    parts = parse.urlparse(url)
    scheme = parts.scheme or 'http'
    url_result = scheme + '://' + parts.netloc + parts.path
    query_dict = dict(parse.parse_qsl(parts.query))
    query_dict.update(query_params)

    if clear_none:
        params_dict = {k: v for k, v in query_dict.items() if v is not None}
    else:
        params_dict = query_dict
    if any(params_dict):
        query_string = parse.urlencode(params_dict)
        url_result = url_result + '?' + query_string

    if any(parts.fragment):
        url_result = url_result + '#' + parts.fragment

    return url_result


def build_query_string(params):
    """
    Build query string with format key1=value1&key2=value2...
    :param params: dictionary of parameters
    :return: query string
    """
    if not isinstance(params, dict):
        params = dict(params)
    return parse.urlencode(params)
