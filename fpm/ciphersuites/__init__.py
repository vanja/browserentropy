"""Passive SSL client fingerprinting using SSL/TLS handshake analysis.
For this method to work, the web app must be deployed on Apache with
'default-ssl' and 'sslhaf' modules installed/enabled.

TLS Cipher Suite Registry:
- file: tls-parameters-4.csv
- source: http://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml
- last updated: 2015-07-10

TLS Extensions Registry:
- source: http://www.iana.org/assignments/tls-extensiontype-values/tls-extensiontype-values.xml
- last updated: 2016-05-20
"""
