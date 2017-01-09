from models.result_handler import DefaultResultHandler


class FontsResultHandler(DefaultResultHandler):
    def format_property(self, property_name, property_value):
        template = '<strong>Detection method: {0}</strong><br/><br/>{1}'

        if property_name == 'fonts':
            for m in ['JavaScript', 'Flash']:
                try:
                    fonts, method = property_value.split('(via {0})'.format(m))
                except ValueError:
                    pass
                else:
                    return template.format(m, fonts)

        return property_value
