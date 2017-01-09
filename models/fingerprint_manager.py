import datetime
import uuid

import bottle

import constants
import log
import repository
import resources
from models import fingerprint as models_fingerprint
from repository import factory

logger = log.get_logger(__name__)


class FingerprintManager(object):
    def __init__(self, config):
        self.config = config
        self.repo = factory.create_repository(self.config)
        assert isinstance(self.repo, repository.Repository)

    def add_fingerprint(self, request_object):
        """Create and persist fingerprints to repository.

        :param request_object: bottle request object containing HTTP headers
        and JSON payload from client
        :type request_object: bottle.LocalRequest
        """
        try:
            now = datetime.datetime.now()
            if now.minute > 30:
                now += datetime.timedelta(hours=1)
            timestamp = now.replace(minute=0, second=0, microsecond=0)

            ip_address = self.get_ip_address(self.config.HASH, request_object)

            try:
                javascript_enabled = request_object.json is not None
            except AttributeError:
                javascript_enabled = False

            try:
                fp_id = request_object.cookies.get(constants.FP_ID)
                fingerprint_id = uuid.UUID(fp_id).hex
                cookies_enabled = True
            except ValueError:
                # in case the cookie has been manually altered
                fingerprint_id = uuid.uuid4().hex
                cookies_enabled = True
            except (AttributeError, TypeError):
                # set uuid manually
                fingerprint_id = uuid.uuid4().hex
                cookies_enabled = False

            fp_methods = resources.registered_methods
            if not javascript_enabled:
                fp_methods = list(
                    filter(lambda m: not m.client_side, fp_methods))

            results = self.parse_client_results(fp_methods, request_object)

            fingerprint = models_fingerprint.Fingerprint(
                fp_id=fingerprint_id,
                timestamp=timestamp,
                ip_address=ip_address,
                cookies_enabled=cookies_enabled,
                js_enabled=javascript_enabled,
                fp_values=results
            )

            if self.exists(fingerprint):
                pass  # skip saving
            else:
                self.save(fingerprint)

            fingerprint.count = self.get_count()
            fingerprint.identical_count = \
                self.get_identical_count(fingerprint)
            fingerprint.figures = self.get_figures(fingerprint)
        except Exception as e:
            logger.error('Could not create fingerprint. {0}'.format(e))
            raise FingerprintException(e)

        return fingerprint

    # END __init__

    def exists(self, fingerprint):
        """check if fingerprint exists in the repository.

        :type fingerprint: models_fingerprint.Fingerprint
        :return:
        """
        return self.repo.is_returning(fingerprint)

    def save(self, fingerprint):
        """Save to repository.

        :type fingerprint: models_fingerprint.Fingerprint
        :return: True if save successful; otherwise False
        :rtype: bool
        """
        obj_id = self.repo.save_fingerprint(fingerprint)
        return obj_id is not None  # success

    def get_identical_count(self, fingerprint):
        """Get number of identical fingerprints

        :type fingerprint: models_fingerprint.Fingerprint
        """
        return self.repo.identical_count(fingerprint)

    def get_count(self):
        """Get total fingerprints count.
        """
        return self.repo.fingerprint_count()

    def get_figures(self, fingerprint):
        """Get frequency of property values for each property in fingerprint.
        These will later be used in ResultRenderer.

        :type fingerprint: models_fingerprint.Fingerprint
        """
        try:
            figures = {
                constants.COOKIES_ENABLED: self.repo.property_count(
                    constants.COOKIES_ENABLED,
                    fingerprint.cookies_enabled
                ),
                constants.JS_ENABLED: self.repo.property_count(
                    constants.JS_ENABLED,
                    fingerprint.js_enabled
                )
            }

            for fpm_id, fpm_result in fingerprint.values.items():
                figures_part = {}
                for prop, value in fpm_result.items():
                    figures_part[prop] = self.repo.property_count(
                        '{0}.{1}'.format(fpm_id, prop), value)
                figures[fpm_id] = figures_part

            return figures
        except ValueError:
            return None

    @staticmethod
    def parse_client_results(fp_methods, request_object):
        """Parse JSON results from client and pack them into a dict with
        method name (str) as key and fingerprint values (OrderedDict).
        :type fp_methods: list
        :type request_object: LocalRequest
        :rtype: dict
        """
        results = dict(
            (method.id,
             method.result_handler_resolved.parse_results(request_object))
            for method in fp_methods
        )
        return results

    @staticmethod
    def get_ip_address(hsh, request_object):
        """Retrieve remote IP address and hash it.

        :type hsh: str
        :type request_object: bottle.LocalRequest
        :return: hashed IP address
        :rtype: str
        """
        import hashlib

        ip_address = request_object.remote_addr
        # or use WSGI environ variables directly:
        # ip_address = request.environ.get('REMOTE_ADDR')

        return hashlib.sha256(hsh.encode() + ip_address.encode()).hexdigest()

    @staticmethod
    def is_debug_mode():
        import sys
        return '--debug' in sys.argv[1:]


class FingerprintException(Exception):
    pass
