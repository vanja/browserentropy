import datetime
import uuid


class Fingerprint(object):
    def __init__(self, fp_id, timestamp, ip_address, cookies_enabled,
                 js_enabled, fp_values, fp_figures=None, count=-1):
        """Fingerprint object.

        :type fp_id: uuid.UUID
        :type timestamp: datetime.datetime
        :type ip_address: str
        :type cookies_enabled: bool
        :type js_enabled: bool
        :type fp_values: dict
        :type fp_figures: dict
        """
        self.id = fp_id
        self.timestamp = timestamp
        self.ip_address = ip_address
        self.cookies_enabled = cookies_enabled
        self.js_enabled = js_enabled
        self.values = fp_values
        self.figures = fp_figures
        self.count = count

        self.identical_count = True
