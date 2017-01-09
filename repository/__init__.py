"""Package for db repository.
"""


class Repository(object):
    """Abstract repository class.

    """
    def fingerprint_count(self):
        pass

    def property_count(self, property_name, property_value):
        pass

    def save_fingerprint(self, fingerprint):
        pass

    def identical_count(self, fingerprint):
        pass

    def is_returning(self, fingerprint):
        pass

    def create_indexes(self, properties):
        pass
