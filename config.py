import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# directory where fingerprinting methods are stored
FP_SUBDIR = 'fpm'
# default name of the fingerprinting method metadata-file
FP_DESC = 'method_info.json'
# default name of the module containing the class for handling results
RESULT_MDL = 'result_handler'

# repository
REPOSITORY_NAME = 'mongodb'
MONGODB_HOST = 'localhost'
MONGODB_DATABASE = 'fp'
MONGODB_COLLECTION = 'fingerprints'
MONGODB_USEAUTH = False
# MONGODB_USERNAME = ''
# MONGODB_PASSWORD = ''

# for hashing ip addresses
HASH = 'changeme'

# reference jQuery from CDN
USE_CDN = False

# mod_sslhaf custom header name
HEADER_FW_CS = 'X-Custom-Header-CipherSuites'
