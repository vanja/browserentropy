import uuid
from collections import OrderedDict

import bottle

import config
import resources


class FingerprintMethod(object):
    def __init__(self, dct, subdir=None):
        """Fingerprint method metadata.

        :param dct: Fingerprint method metadata in form of a JSON dictionary
        :type dct: dict
        """
        if 'id' in dct and dct['id']:
            self.id = dct['id']
        else:
            raise ValueError('Fingerprint method must specify an \'id\'!')

        if 'name' in dct and dct['name']:
            self.name = dct['name']
        else:
            raise ValueError('Fingerprint method must specify a \'name\'!')

        if 'order' in dct:
            self.order = int(dct['order'])
        else:
            self.order = 10000

        if 'result_handler' in dct and dct['result_handler']:
            self.result_handler = dct['result_handler']
        else:
            self.result_handler = None

        if 'client_side' in dct \
                and str(dct['client_side']).lower() == 'false':
            self.client_side = False
        else:
            self.client_side = True

        if 'template' in dct and dct['template']:
            self.template = dct['template']
        else:
            self.template = None

        if 'js' in dct and dct['js']:
            self.js = dct['js']
        else:
            self.js = None

        if 'scripts' in dct and dct['scripts']:
            self.scripts = dct['scripts']
        else:
            self.scripts = []

        if 'static' in dct and dct['static']:
            self.static_files = dct['static']
        else:
            self.static_files = []

        if 'properties' in dct and dct['properties']:
            self.properties = OrderedDict(dct['properties'])
        else:
            self.properties = OrderedDict()

        if 'hashed_properties' in dct and dct['hashed_properties']:
            self.hashed_properties = OrderedDict(dct['hashed_properties'])
        else:
            self.hashed_properties = OrderedDict()

        self.subdir = subdir

        self.runtime_id = str(uuid.uuid4().hex)

    @property
    def result_handler_resolved(self):
        """Use result handler specified in the fingerprint method metadata,
        otherwise fall back to default result handler.

        :return: Instance of ResultHandler
        """
        if self.result_handler is not None:
            class_name = '.'.join([
                config.FP_SUBDIR,
                self.subdir,
                config.RESULT_MDL,
                self.result_handler
            ])

            handler_class = resources.load_class(class_name)
            assert handler_class is not None

            handler_instance = handler_class(fingerprint_method=self)
            assert handler_instance is not None

            return handler_instance
        else:
            from models.result_handler import DefaultResultHandler
            return DefaultResultHandler(fingerprint_method=self)

    def parse_results(self, request_object):
        """
        :type request_object: bottle.LocalRequest
        :rtype: OrderedDict
        """
        return self.result_handler_resolved.parse_results(request_object)
