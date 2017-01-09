import collections


HEADERS_ORDER = 'order'
HTTP_HEADERS = (('ua', 'User-Agent'),
                ('accept', 'Accept'),
                ('accept_enc', 'Accept-Encoding'),
                ('accept_lang', 'Accept-Language'),
                ('connection', 'Connection'))


def http_headers(request_headers):
    headers = dict((p, request_headers.get(k, 'n/a')) for p, k in
                   collections.OrderedDict(HTTP_HEADERS).items())
    headers[HEADERS_ORDER] = headers_order(request_headers)
    return headers


def headers_order(request_headers):
    return ', '.join(h for h in request_headers
                     if h in dict(HTTP_HEADERS).values())
