import collections
import json
import os
from models.result_handler import DefaultResultHandler

DESC_FILE = os.path.join(os.path.dirname(__file__), 'modernizr-properties.json')
SEPARATOR = '__'
DEFAULT_VALUE = 5  # unknown


class HTML5ResultHandler(DefaultResultHandler):
    @property
    def properties(self):
        with open(DESC_FILE, 'r') as f:
            props_json = json.loads(f.read(),
                                    object_pairs_hook=collections.OrderedDict)

        props = collections.OrderedDict()
        for prop, val in props_json['properties'].items():
            if isinstance(val, dict):
                desc_base = ''
                for name, desc in val.items():
                    if name == SEPARATOR:  # e.g. 'audio'
                        desc_base = desc
                        props[str(prop)] = str(desc)
                    else:  # e.g. 'audio__mp3'
                        props['{0}{2}{1}'.format(prop, name, SEPARATOR)] = \
                            '{0} ({1})'.format(desc_base, desc) if desc_base \
                            else desc
            else:
                props[str(prop)] = str(val)

        return props

    def parse_results(self, request_object):
        res_part = self.get_result_part(request_object)

        props = collections.OrderedDict(
            (p, res_part.get(p, DEFAULT_VALUE)) for p in self.properties.keys())

        # TODO: add hashed property
        return props

    def format_property(self, property_name, property_value):
        switcher = {
            0: 'False',
            1: 'True',
            2: 'Probably',
            3: 'Maybe'
        }

        return switcher.get(property_value, 'Unknown')
