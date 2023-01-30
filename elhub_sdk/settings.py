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


# ENVIRONMENT DEPENDING CONSTANTS, deprecated
WSDL_FILES_CONFIG = {
    # This is meant to be used against SoapUI Mock services or ElHub environment
    "QUERY": getenv("WSDL_QUERY", "wsdl/local/2.3/wsdl/Query.wsdl"),
    "POOL_METERING": getenv("WSDL_POOL_METERING", "wsdl/local/2.3/wsdl/PollMeteringValues.wsdl"),
    "MARKET_PROCESSES": getenv("WSDL_MARKET_PROCESSES", "wsdl/local/2.3/wsdl/MarketProcesses.wsdl"),
}

# This is meant to be used against Exatest2, deprecated
WSDL_FILES_CONFIG_TEST = {
    "QUERY": getenv("WSDL_QUERY", "wsdl/test/2.3/wsdl/Query - WS-Security.wsdl"),
    "POOL_METERING": getenv("WSDL_POOL_METERING", "wsdl/test/2.3/wsdl/PollMeteringValues - WS-Security.wsdl"),
    "MARKET_PROCESSES": getenv("WSDL_MARKET_PROCESSES", "wsdl/test/2.3/wsdl/MarketProcesses - WS-Security.wsdl"),
}
