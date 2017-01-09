import cgi
import math

import resources
from models import fingerprint, fingerprint_method


def alert_message(fp):
    if fp.identical_count == 1:
        msg = 'Your browser appears to be unique among ' \
              '{0} collected fingerprints!'
        return 'danger', msg.format(fp.count)

    msg = 'You are {0} unique! ' \
          '{1} out of {2} collected fingerprints are same as yours.'
    if float(fp.identical_count) / float(fp.count) < 0.05:
        return 'warning', msg.format('almost', fp.identical_count, fp.count)
    else:
        return 'success', msg.format('not', fp.identical_count, fp.count)


def fp_results(fp):
    """Result generator which iterates through all fingerprinting methods'
     results and for every result yields a list of properties (including
     names, values and figures - entropy, uniqueness, etc.) alongside the
     method's name. The results are then utilized in the result_table.tpl
     template.

    :type fp: fingerprint.Fingerprint
    """
    fp_methods = resources.registered_methods
    if not fp.js_enabled:
        fp_methods = list(filter(lambda m: not m.client_side, fp_methods))

    for fpm in sorted(fp_methods, key=lambda m: m.order):
        assert isinstance(fpm, fingerprint_method.FingerprintMethod)
        rh = fpm.result_handler_resolved

        # kil1 me now pls
        yield list((p_desc,
                    format_property(p_name, fp.values[fpm.id][p_name], rh),
                    format_figures(fp.figures[fpm.id][p_name], fp.count))
                   for p_name, p_desc in rh.ordered_properties), fpm.name


def escape_html(prop):
    if isinstance(prop, str) or isinstance(prop, unicode):
        return cgi.escape(prop).encode('utf-8')
    else:
        return prop


def format_property(property_name, property_value, result_handler):
    return result_handler.format_property(property_name,
                                          escape_html(property_value))


def format_figures(property_count, fp_count):
    percentage = 100 * float(property_count) / float(fp_count)
    uniqueness = float(fp_count) / float(property_count)
    entropy = math.log(uniqueness, 2)

    def fmt(value, precision=2):
        return '<0.1' if 0.0 < value < 0.1 else str(round(value, precision))

    return fmt(uniqueness), fmt(entropy), fmt(percentage)
