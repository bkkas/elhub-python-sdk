"""
Enums, mainly to create SOAP requests
taken from various places in Elhub documentation
"""

from enum import Enum


class LIST_AGENCY_IDENTIFIER(Enum):
    """
    Agency identifier
    """

    EBIX = '260'
    UN_CEFACT = '6'
    ELHUB = '89'


class DOCUMENT_TYPE_EBIX(Enum):
    """
    Metering data: https://dok.elhub.no/ediel200utkast/document-type
    """

    METERING_DATA = "E13"


class DOCUMENT_TYPE_UN_CEFACT(Enum):
    """
    Quaery types
    """

    QUERY = "21"


class SCHEME_AGENCY_IDENTIFIER(Enum):
    """
    Agency identifiers
    """

    GS1 = '9'


class BSR_IDS(Enum):
    """
    Query type
    https://dok.elhub.no/ediel200utkast/elhub-brs-identifications
    """

    METERING_VALUES = "BRS-NO-315"


class ROLES(Enum):
    """
    Roles:
        https://dok.elhub.no/ediel200utkast/roles-and-domains
    """

    THIRD_PARTY = "AG"
    BALANCE_SUPPLIER = "DDQ"


class QUERY_MARKET(Enum):
    """
    https://dok.elhub.no/ediel200utkast/5-query-from-market-parties
    """

    METERING_VALUES_TIME_SERIES = "MVTS"


class ENERGY_INDUSTRY_CLASSIFICATION(Enum):
    """
    Industry codes
    https://dok.elhub.no/ediel200utkast/general
    """

    ELECTRICITY_SUPPLY = "23"
