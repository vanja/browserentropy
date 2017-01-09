import bson.objectid
import pymongo
import pymongo.errors

import constants
import datetime
import log
import repository
from models import fingerprint

logger = log.get_logger(__name__)


class MongoDBRepository(repository.Repository):
    def __init__(self, host_name, database_name, collection_name, auth=None):
        """
        :type host_name: str
        :type database_name: str
        :type collection_name: str
        """
        try:
            self._client = pymongo.MongoClient(host_name)
        except pymongo.errors.PyMongoError as e:
            logger.error(
                'Could not connect to server: {0}\n{1}'.format(host_name, e))
        else:
            if auth:
                self._client[database_name].authenticate(auth[0], auth[1])
            self._collection = self._client[database_name][collection_name]

    def fingerprint_count(self):
        """Return total count of fingerprints.

        :rtype: int
        """
        try:
            count = self._collection.count()
            return 0 if count is None else count
        except pymongo.errors.PyMongoError as e:
            logger.error('{0} {1}'.format(e.__class__.__name__, e.message))
            return 0

    def property_count(self, property_name, property_value):
        """Get statistics for property with given value.

        :type property_name: str
        :type property_value: object
        :return: (uniqueness, bits of entropy) as tuple
        :rtype: tuple
        """
        try:
            return self._collection.count({property_name: property_value})
        except pymongo.errors.PyMongoError as e:
            logger.error('No occurrences of \'{0}\' = \'{1}\' found; '
                         'should save first. {2}'.format(property_name,
                                                         property_value,
                                                         e.message))
            return 0

    def save_fingerprint(self, fp):
        """Persist fingerprint to repository.

        :param fp: Fingerprint to persist
        :type fp: fingerprint.Fingerprint
        :rtype: bson.objectid.ObjectId
        """
        fp_doc = dict(fp.values)
        fp_doc.update({
            constants.TIMESTAMP: fp.timestamp,
            constants.IP_ADDR: fp.ip_address,
            constants.FP_ID: str(fp.id),
            constants.COOKIES_ENABLED: fp.cookies_enabled,
            constants.JS_ENABLED: fp.js_enabled,
        })

        try:
            result = self._collection.insert_one(fp_doc)
            assert isinstance(result.inserted_id, bson.objectid.ObjectId)
            return result.inserted_id
        except (pymongo.errors.PyMongoError, AssertionError) as e:
            logger.error('Could not save fingerprint.\n{0}: {1}'.format(
                e.__class__.__name__, e.message))
            return None

    def identical_count(self, fp, cookies=True):
        """Return the number of identical fingerprints by comparing all
        values.

        :param fp: Fingerprint to compare
        :type fp: fingerprint.Fingerprint
        :rtype: bool
        """
        fp_doc = self.fingerprint_to_doc(fp, cookies=cookies)
        try:
            return self._collection.count(fp_doc)
        except pymongo.errors.PyMongoError as e:
            logger.error('{0} {1}'.format(e.__class__.__name__, e.message))
            return 0

    def is_returning(self, fp):
        """ Check if the fingerprint is already present in the repository.
        There are two scenarios to consider:
        1) Cookies are enabled - check if fingerprints exists with same
        cookie id *and* same values. In case the values have changed the
        fingerprint gets persisted again.
        2) Cookies are disabled - in order to avoid persisting duplicates
        check if fingerprints exist with same values, IP address and
        timestamp between now and $hours$ in the past.


        :param fp: Fingerprint to check
        :type fp: fingerprint.Fingerprint
        :rtype: bool
        """
        hours = 12

        try:
            fp_doc = self.fingerprint_to_doc(fp, cookies=False)
            if fp.cookies_enabled:
                fp_doc[constants.FP_ID] = str(fp.id)
            else:
                fp_doc[constants.IP_ADDR] = fp.ip_address
                fp_doc[constants.TIMESTAMP] = {
                    '$lte': fp.timestamp + datetime.timedelta(hours=1),
                    '$gte': fp.timestamp - datetime.timedelta(hours=hours)}
                # [past, timestamp)

            result = self._collection.count(fp_doc)
            return result != 0
        except pymongo.errors.PyMongoError as e:
            logger.error('{0} {1}'.format(e.__class__.__name__, e.message))
            return False

    @staticmethod
    def fingerprint_to_doc(fp, cookies=True):
        """
        :type fp: fingerprint.Fingerprint
        :return:
        """
        fp_doc = {
            constants.JS_ENABLED: fp.js_enabled
        }

        for fpm_id, fpm_result in fp.values.items():
            for prop, value in fpm_result.items():
                fp_doc['{0}.{1}'.format(fpm_id, prop)] = value

        if cookies:
            fp_doc[constants.COOKIES_ENABLED] = fp.cookies_enabled

        return fp_doc

    def create_indexes(self, properties):
        logger.info('using mongodb repository \'{0}\''
                    .format(self._collection.name))

        try:
            for prop in properties:
                logger.info('creating hashed index on \'{0}\''.format(prop))
                self._collection.create_index([(prop, pymongo.HASHED)])
        except pymongo.errors.PyMongoError as e:
            logger.error('{0} {1}'.format(e.__class__.__name__, e.message))
