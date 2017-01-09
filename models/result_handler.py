from collections import OrderedDict

import bottle

import constants
from models import fingerprint_method as fp_method


class DefaultResultHandler(object):
    """This class serves two purposes:
    a) handle fingerprinting results for a specific fingerprinting method and
       prepare the values for persistence,
    b) format the values suitable for HTML presentation when displaying
    fingerprinting results.

    Every fingerprinting method can declare its own result handler and
    overwrite the methods as necessary.
    """
    def __init__(self, fingerprint_method):
        """
        :type fingerprint_method: fp_method.FingerprintMethod
        """
        self.fpm_id = fingerprint_method.id
        self.fpm_name = fingerprint_method.name
        self.fpm_rid = fingerprint_method.runtime_id
        self.fpm_properties = fingerprint_method.properties
        self.fpm_hashed_properties = fingerprint_method.hashed_properties

    @property
    def properties(self):
        """
        :rtype: dict
        """
        return self.fpm_properties

    @property
    def hashed_properties(self):
        """
        :rtype: dict
        """
        return self.fpm_hashed_properties

    @property
    def ordered_properties(self):
        return self.properties.items() + self.hashed_properties.items()

    def get_result_part(self, request_object):
        """Parse JSON result and return the part relevant for this particular
        fingerprint method.
        :type request_object: bottle.LocalRequest
        :return: dict
        """
        result_root = request_object.json.get(constants.FP_ROOT, None)
        assert result_root is not None

        fpm_result = result_root.get(self.fpm_rid, None)
        assert fpm_result is not None
        return fpm_result

    def parse_results(self, request_object):
        """Parse results from JSON and save them in an OrderedDict with
        fingerprint property names as keys.
        :type request_object: LocalRequest
        :return: OrderedDict
        """
        result_part = self.get_result_part(request_object)
        try:
            props = OrderedDict((p, result_part[p])
                                for p in self.properties.keys())

            props.update((p, result_part[p])
                         for p in self.hashed_properties.keys())

            return props
        except KeyError as e:
            # don't temper with the results
            raise ValueError('Property \'{0}\' missing in \'{1}\' result'
                             .format(e, self.fpm_name))

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def format_property(self, property_name, property_value):
        return property_value
