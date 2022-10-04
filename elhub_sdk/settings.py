"""
    Settings module
"""
import logging.config
from os import getenv

logging.config.dictConfig(
    {
        'version': 1,
        'formatters': {'verbose': {'format': '%(name)s: %(message)s'}},
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'zeep.transports': {
                'level': 'DEBUG',
                'propagate': True,
                'handlers': ['console'],
            },
        },
    }
)

# Key and cert files for signing to Elhub
KEY_FILE = getenv("ELHUB_KEY_FILE")
CERT_FILE = getenv("ELHUB_CERT_FILE")

# Third party GSN
THIRD_PARTY_GSN = getenv("THIRD_PARTY_GSN", None)

ENVIRONMENT = getenv("ENVIRONMENT", "LOCAL")  # LOCAL TEST PROD


# ENVIRONMENT DEPENDING CONSTANTS
WSDL_FILES_CONFIG = {
    "LOCAL": {  # This is meant to be used against SoapUI Mock services
        "QUERY": "wsdl/local/2.3/wsdl/Query.wsdl",
        "POOL_METERING": "wsdl/local/2.3/wsdl/PollMeteringValues.wsdl",
    },
    "TEST": {  # This is meant to be used against test services
        "QUERY": "wsdl/test/2.3/wsdl/Query.wsdl",
        "POOL_METERING": "wsdl/test/2.3/wsdl/PollMeteringValues.wsdl",
    },
}

SECURE_CONFIG = {
    "LOCAL": False,
    "TEST": True,
    "PROD": True,
}

WSDL_FILES = WSDL_FILES_CONFIG[ENVIRONMENT]

SECURE = SECURE_CONFIG[ENVIRONMENT]
