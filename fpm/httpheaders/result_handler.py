import bottle

import collections
import headers_util
from models.result_handler import DefaultResultHandler

JSON_ELEMENT = 'headers'


class HttpHeadersHandler(DefaultResultHandler):
    @property
    def headers(self):
        props = collections.OrderedDict(headers_util.HTTP_HEADERS)
        props[headers_util.HEADERS_ORDER] = 'Headers Order'
        ua = {'ua': props.pop('ua')}

        return ua, props  # hashed, normal

    @property
    def properties(self):
        return self.headers[1]

    @property
    def hashed_properties(self):
        return self.headers[0]

    @property
    def ordered_properties(self):
        return self.hashed_properties.items() + self.properties.items()

    def get_result_part(self, request_obj):
        """HTTP headers are forwarded from GET /fp to POST /fp by being
        embedded in the JSON payload (in *JSON_ELEMENT*) in case when JS is
        enabled, otherwise they can be found in the headers dict of the
        request object.

        :type request_obj: bottle.LocalRequest
        """
        if request_obj.json:
            return request_obj.json[JSON_ELEMENT]

        return headers_util.http_headers(request_obj.headers)

    def format_property(self, property_name, property_value):
        if property_name == 'accept' or property_name == 'ua':
            return str(property_value).replace('/', u'/\u200B')  # break on '/'

        if property_name == 'accept_lang':
            return str(property_value).replace(';', u';\u200B')  # break on ';'

        return property_value
