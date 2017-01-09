from models import result_handler


class HtmlCanvasResultHandler(result_handler.DefaultResultHandler):
    def format_property(self, property_name, property_value):
        if property_name == 'img':
            if not str(property_value).startswith('data:image/png;base64'):
                return property_value

            return '<img src="{0}" title="canvas" ' \
                   'class="img-responsive">'.format(str(property_value))
