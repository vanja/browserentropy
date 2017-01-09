from models.result_handler import DefaultResultHandler

LIST_ENTRY_TPL = '<dt>{0}</dt><dd>{1}<br/>MimeTypes: {2}</dd><br/>'
LIST_IE_TPL = '<dt>{0}</dt><br/>'


class PluginsResultHandler(DefaultResultHandler):
    def format_property(self, property_name, property_value):
        if property_name == 'dnt':
            return str(property_value).capitalize()

        if property_name == 'plugins':
            if not str(property_value).strip():
                return 'No plugins detected'

            plugins = str(property_value).split('|||\r\n')
            if not isinstance(plugins, list):
                return plugins

            result = ''
            for p in plugins:
                try:
                    result += LIST_ENTRY_TPL.format(*p.split('::'))\
                        .replace('<dd><br/>', '<dd>')\
                        .replace('~,', ', ')\
                        .replace('~', ' ')
                except IndexError:  # IE
                    result += LIST_IE_TPL.format(p)

            # class="dl-horizontal"
            return '<dl>{0}</dl>'.format(result.rstrip('<br/>'))

        return property_value
