import json
import os
import uuid

from bottle import error, request, response, route, static_file, template, \
    SimpleTemplate

import config
import constants
import headers_util
import log
import resources as res
from models import fingerprint_manager

logger = log.get_logger(__name__)
SimpleTemplate.defaults['url'] = lambda: str(request.url).split('/')[-1]


@route('/')
def index():
    fp_manager = fingerprint_manager.FingerprintManager(config)
    return template('index', fp_count=fp_manager.get_count())


@route('/fp')
def fp():
    set_cookie()
    headers = headers_util.http_headers(request.headers)
    return template('fp',
                    referenced_scripts=res.referenced_scripts,
                    registered_methods=res.registered_methods,
                    headers='headers: {0}'.format(json.dumps(headers)))


@route('/fpnojs')
def fpnojs():
    set_cookie()

    fingerprint = process_result(request)
    if not fingerprint:
        return ''

    return template('result_table', fp=fingerprint, no_js=True)


@route('/fp', method='POST')
def post_fp():
    fingerprint = process_result(request)
    if not fingerprint:
        return ''

    return template('result_table', fp=fingerprint)


def process_result(request_obj):
    try:
        fp_manager = fingerprint_manager.FingerprintManager(config)
        return fp_manager.add_fingerprint(request_obj)
    except fingerprint_manager.FingerprintException:
        import pprint
        logger.error(pprint.pformat({
            'Cookies': request.cookies.get(constants.FP_ID),
            'JSON': request.json,
            'HTTP Headers': dict(
                (k, v) for k, v in request.headers.environ.items() if
                'HTTP' in k or 'X-' in k)
            }, indent=2)
        )

        return None


@route('/about')
def about():
    return template('about')


@route('/contact')
def about():
    return template('contact')


@route('/privacy')
def privacy():
    return template('privacy')


@route('/static/<subdir>/<filename:path>')
def static_files(subdir, filename):
    """ Serve static files in
     '/static/css/*', '/static/fonts/*' and '/static/js/*'.
    """
    if subdir in ['css', 'fonts', 'img', 'js']:
        return static_file(filename, res.project_subdir('static/' + subdir))


@route('/<fp_subdir>/<method>/<filename:path>')
def fpmethod_static(fp_subdir, method, filename):
    """Serve fingerprint methods' specific static files.
    """
    if fp_subdir != config.FP_SUBDIR:
        pass

    # e.g. filename: 'js/navigator.js'
    parts = [fp_subdir, method] + list(os.path.split(filename))
    if '/'.join(parts) in res.referenced_scripts+res.referenced_static_files:
        return static_file(
            parts[-1],
            res.project_subdir(os.path.join(*parts[:-1])))


@error(404)
def error404(e):
    """Error handling.

    :return blank page
    """
    return str(e)


def set_cookie():
    """Set cookie for 90 days.
    """
    if not request.cookies.get(constants.FP_ID):
        response.set_cookie(
            name=constants.FP_ID,
            value=uuid.uuid4().hex,
            max_age=constants.COOKIE_AGE
        )


# reference to app.py -- DO NOT REMOVE!
refd = False
