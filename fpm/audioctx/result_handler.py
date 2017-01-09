from models.result_handler import DefaultResultHandler


class AudioContextResultHandler(DefaultResultHandler):
    def format_property(self, property_name, property_value):
        if property_name == 'ac_props' and property_value != 'n/a':
            result = ''
            props = property_value.split('|||')
            for p in props:
                try:
                    result += '<li>{0}: {1}</li>'.format(*p.split('::'))
                except IndexError:
                    return property_value

            return '<ul class="list-unstyled">{0}</ul>'.format(result)

        return property_value
