import bottle
import csv
import os
import config
from models.result_handler import DefaultResultHandler

CSV_FILE = os.path.join(os.path.dirname(__file__), 'tls-parameters-4.csv')


class CipherSuitesResultHandler(DefaultResultHandler):
    _cipher_dict = None

    def get_result_part(self, request_object):
        """
        :type request_object: bottle.LocalRequest
        """
        # for testing purposes
        # custom_header = '"3" \t\t"3.3" "c030,c02c,c028,c024,c014,c00a,a3,' \
        #                 '9f,6b,6a,39,38,88,87,c032,c02e,c02a,c026,c00f,' \
        #                 'c005,9d,3d,35,84,c012,c008,16,13,c00d,c003,0a,' \
        #                 'c02f,c02b,c027,c023,c013,c009,a2,9e,67,40,33,32,' \
        #                 '9a,99,45,44,c031,c02d,c029,c025,c00e,c004,9c,3c,' \
        #                 '2f,96,41,ff" "00" \t\t"0000,000b,000a,000d,000f" ' \
        #                 '"i=80"'

        custom_header = request_object.get_header(config.HEADER_FW_CS, '')
        parts = custom_header.replace('\"', '').replace('\t', '').split(' ')
        result = dict((p, '') for p in
                      self.properties.keys() + self.hashed_properties.keys())

        try:
            result['handshake_ver'] = parts[0]
            result['protocol_ver'] = parts[1]
            result['cipher_suites'] = parts[2]
            result['compression'] = parts[3]
            result['extensions'] = parts[4]
        except IndexError:
            pass

        return result

    def format_property(self, property_name, property_value):
        if not property_value:
            return 'n/a'

        def parse_value(di):
            """
            :type di; dict
            """
            return di.get(property_value,
                          'can\'t parse ({0})'.format(property_value))

        if property_name == 'handshake_ver':
            return parse_value({
                '2': 'SSL v2',
                '3': 'SSL v3+'
            })

        if property_name == 'protocol_ver':
            return parse_value({
                '3.0': 'SSLv3',
                '3.1': 'TLS 1.0',
                '3.2': 'TLS 1.1',
                '3.3': 'TLS 1.2',
                '3.4': 'TLS 1.3'
            })

        if property_name == 'compression':
            return parse_value({
                '-': 'NULL',
                '00': 'NULL',
                '01': 'DEFLATE'
            })

        if property_name == 'cipher_suites':
            if not property_value:
                return 'n/a'

            def format_as_bytes(s):
                s = s.zfill(4).upper()
                return '0x{0},0x{1}'.format(s[0:2], s[-2:])

            cipher_bytes = list(
                format_as_bytes(p) for p in str(property_value).split(',')
            )

            return ', '.join(
                self.cipher_dict.get(cb, 'UNKNOWN ({0})'.format(cb))
                for cb in cipher_bytes
            )

        if property_name == 'extensions':
            ex = {'0000': 'server_name',
                  '0001': 'max_fragment_length',
                  '0002': 'client_certificate_url',
                  '0003': 'trusted_ca_keys',
                  '0004': 'truncated_hmac',
                  '0005': 'status_request',
                  '0006': 'user_mapping',
                  '0007': 'client_authz',
                  '0008': 'server_authz',
                  '0009': 'cert_type',
                  '000a': 'supported_groups',
                  '000b': 'ec_point_formats',
                  '000c': 'srp',
                  '000d': 'signature_algorithms',
                  '000e': 'use_srtp',
                  '000f': 'heartbeat',
                  '0010': 'application_layer_protocol_negotiation',
                  '0011': 'status_request_v2',
                  '0012': 'signed_certificate_timestamp',
                  '0013': 'client_certificate_type',
                  '0014': 'server_certificate_type',
                  '0015': 'padding',
                  '0016': 'encrypt_then_mac',
                  '0017': 'extended_master_secret',
                  '0018': 'token_binding',
                  '0019': 'cached_info',
                  # ...
                  '0023': 'SessionTicket TLS',
                  # ...
                  'ff01': 'renegotiation_info'}
            return ', '.join([ex.get(e, 'unassigned ({0})'.format(e))
                              for e in property_value.split(',')])

        return property_value

    @property
    def cipher_dict(self):
        if self._cipher_dict is None:
            try:
                with open(CSV_FILE, 'r') as f:
                    self._cipher_dict = dict(
                        {row[0]: row[1] for row in csv.reader(f)}
                    )
            except IOError:
                self._cipher_dict = dict()

        return self._cipher_dict
