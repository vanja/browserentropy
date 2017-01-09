from models import result_handler

DEFAULT_VALUE = 'n/a'


class WebGLResultHandler(result_handler.DefaultResultHandler):
    def get_result_part(self, request_object):
        result_part = super(WebGLResultHandler,
                            self).get_result_part(request_object)

        result_part.update(
            (p, DEFAULT_VALUE) for p in
            self.properties.keys() + self.hashed_properties.keys()
            if p not in result_part
        )

        return result_part
