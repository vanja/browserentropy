import json
import os
from collections import OrderedDict

from bottle import TEMPLATES, TEMPLATE_PATH

import config
import log
from models import fingerprint_method
from repository import factory

logger = log.get_logger(__name__)
registered_methods = []
referenced_scripts = []
referenced_static_files = []


def __reference_scripts():
    # empty the list in case of reinitialization
    referenced_scripts[:] = []

    # reference modernizr, since it's used by different fingerprinting methods
    referenced_scripts.append('static/js/modernizr-custom.min.js')
    referenced_scripts.append('static/js/json3.min.js')

    for method in [m for m in registered_methods if m.scripts]:
        for script in method.scripts:
            script_name = '{0}/{1}/{2}'.format(
                unicode(config.FP_SUBDIR),
                unicode(method.subdir),
                unicode(script)
            ).replace('//', '/')
            referenced_scripts.append(script_name)

    logger.info('scripts referenced')


def __reference_static_files():
    for method in [m for m in registered_methods if m.static_files]:
        for static_file in method.static_files:
            script_file_name = '{0}/{1}/{2}'.format(
                unicode(config.FP_SUBDIR),
                unicode(method.subdir),
                unicode(static_file)
            ).replace('//', '/')
            referenced_static_files.append(script_file_name)

    logger.info('static files referenced')


def __register_methods():
    # empty the list in case of reinitialization
    registered_methods[:] = []

    for fpm_dir in os.walk(project_subdir(config.FP_SUBDIR)).next()[1]:
        desc_file = project_subdir(
            os.path.join(config.FP_SUBDIR, fpm_dir, config.FP_DESC))
        if not os.path.isfile(desc_file):
            msg = '\'method_info.json\' is missing in \'{0}\'. skipped'
            logger.warn(msg.format(fpm_dir))
            continue
        try:
            with open(desc_file, 'r') as f:
                fpm = json.loads(f.read(), object_pairs_hook=OrderedDict)

            fpm = fingerprint_method.FingerprintMethod(fpm, fpm_dir)
            registered_methods.append(fpm)
            msg = 'successfully loaded method from \'{0}\''
            logger.info(msg.format(fpm_dir))
        except Exception as e:
            msg = 'could not load method from \'{0}\'. {1}'
            logger.error(msg.format(fpm_dir, e))
            continue
        finally:
            f.close()

    logger.info('fingerprint methods registered')


def __update_template_path():
    # Sometimes, when caching templates bottle doesn't clear the faulty
    # templates and the error persists even upon restarting the app.
    # The solution is to clear the templates explicitly with this statement:
    TEMPLATES.clear()

    for m in registered_methods:
        method_path = unicode('./{0}/{1}/'.format(config.FP_SUBDIR, m.subdir))
        if method_path not in TEMPLATE_PATH:
            TEMPLATE_PATH.insert(0, method_path)

    logger.info('updated TEMPLATE_PATH')


def __create_db_indexes():
    prop_names = []
    for m in registered_methods:
        assert isinstance(m, fingerprint_method.FingerprintMethod)
        for prop in m.result_handler_resolved.hashed_properties:
            prop_names.append('{0}.{1}'.format(m.id, prop))

    prop = factory.create_repository(config)
    prop.create_indexes(prop_names)

    logger.info('created all indexes')


def initialize():
    """Initialize resources on startup.

    Register all valid fingerprinting methods contained in FP_SUBDIR and
    reference corresponding javascript files which will be embedded in HTML.
    """
    __register_methods()
    __reference_scripts()
    __reference_static_files()
    __update_template_path()
    __create_db_indexes()
    logger.info('resource initialization complete')


def project_subdir(subdir_name):
    """Return the full path of a subdirectory in the PROJECT_ROOT directory
    """
    return os.path.join(config.PROJECT_ROOT, subdir_name).replace('\\', '/')


def load_class(class_name):
    """Load class using introspection.

    :param class_name: fully qualified class name including package and module
    name(s). E.g. 'fp_methods.html5.result_handler.HTML5Result' will load a
    class 'HTML5Result', contained in the module 'result_handler' from the
    package 'fp_methods.html5'.
    :type class_name: str
    :return: Class object. It is possible to access attributes and functions
    of the returned class by instantiating the class and using the Python
    built-in function 'getattr()'. Example:
        k = kls() # create instance of class 'kls'
        attrib = getattr(k, 'attribute') # access attribute
        result = getattr(k, 'method')()  # run method
    """
    parts = class_name.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m
