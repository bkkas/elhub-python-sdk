"""
Enums, mainly to create SOAP requests
"""
from enum import Enum


class LIST_AGENCY_IDENTIFIER(Enum):
    EBIX = '260'
    UN_CEFACT = '6'
    ELHUB = '89'


class DOCUMENT_TYPE_EBIX(Enum):
    METERING_DATA = "E13"  # Metering data: https://dok.elhub.no/ediel200utkast/document-type


class DOCUMENT_TYPE_UN_CEFACT(Enum):
    QUERY = "21"


class SCHEME_AGENCY_IDENTIFIER(Enum):
    GS1 = '9'


class BSR_IDS(Enum):
    METERING_VALUES = "BRS-NO-315"  # https://dok.elhub.no/ediel200utkast/elhub-brs-identifications


class ROLES(Enum):
    THIRD_PARTY = "AG"  # https://dok.elhub.no/ediel200utkast/roles-and-domains
    BALANCE_SUPPLIER = "DDQ"


class QUERY_MARKET(Enum):  # https://dok.elhub.no/ediel200utkast/5-query-from-market-parties
    METERING_VALUES_TIME_SERIES = "MVTS"


class ENERGY_INDUSTRY_CLASSIFICATION(Enum):  # https://dok.elhub.no/ediel200utkast/general
    ELECTRICITY_SUPPLY = "23"
