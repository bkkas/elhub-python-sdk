"""
Consumption related functions


The data will be made available on the polling service. If the query is related to metering values
(applies to the RequestDataFromElhubRequest message and depends on the specified query type), the responses
(including Acknowledgement) will be made available on the PollMeteringValues service.

"""
import logging
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional

import zeep

from elhub_sdk.client import APIClient
from elhub_sdk.constants import ELHUB_GSN, TIME_FORMAT
from elhub_sdk.enums import (
    BSR_IDS,
    DOCUMENT_TYPE_EBIX,
    DOCUMENT_TYPE_UN_CEFACT,
    LIST_AGENCY_IDENTIFIER,
    QUERY_MARKET,
    ROLES,
    SCHEME_AGENCY_IDENTIFIER,
)
from elhub_sdk.settings import WSDL_FILES

logger = logging.getLogger()


def request_consumption(
    meter_identificator: str, third_party_gsn: str, start: datetime, end: datetime
) -> Optional[dict]:
    """

    Args:
        meter_identificator:
        third_party_gsn:
        start:
        end:

    Returns:

    """
    client, history = APIClient.get_zeep_client(wsdl=WSDL_FILES['QUERY'])

    factory = client.type_factory('ns4')
    eh_request = factory.RequestDataFromElhub(
        Header={
            'Identification': uuid.uuid4(),
            'DocumentType': {
                '_value_1': DOCUMENT_TYPE_EBIX.METERING_DATA.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.EBIX.value,
            },
            'Creation': f'{datetime.utcnow().strftime(TIME_FORMAT)}',
            'PhysicalSenderEnergyParty': {
                'Identification': {
                    '_value_1': third_party_gsn,
                    'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value,
                }
            },
            'JuridicalSenderEnergyParty': {
                'Identification': {
                    '_value_1': third_party_gsn,
                    'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value,
                }
            },
            'JuridicalRecipientEnergyParty': {
                'Identification': {'_value_1': ELHUB_GSN, 'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value}
            },
        },
        ProcessEnergyContext={  # https://dok.elhub.no/ediel200utkast/general#General-Process
            'EnergyBusinessProcess': {
                '_value_1': BSR_IDS.METERING_VALUES.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.ELHUB.value,
            },
            'EnergyBusinessProcessRole': {
                '_value_1': ROLES.THIRD_PARTY.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.UN_CEFACT.value,
            },
            'EnergyIndustryClassification': "23",
        },
        PayloadMPEvent={
            'QueryTypeCode': QUERY_MARKET.METERING_VALUES_TIME_SERIES.value,
            'Period': {'Start': f'{start.strftime(TIME_FORMAT)}', 'End': f'{end.strftime(TIME_FORMAT)}'},
            'MeteringPointUsedDomainLocation': {
                'Identification': {
                    '_value_1': meter_identificator,
                    'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value,
                }
            },
        },
    )

    response = client.service.RequestDataFromElhub(eh_request)
    return response


def poll_consumption(third_party_gsn: str) -> Optional[str]:
    """

    Args:
        third_party_gsn:

    Returns:
        xml document with the consumption
    """
    client, history = APIClient.get_zeep_client(wsdl=WSDL_FILES['POOL_METERING'])
    factory = client.type_factory('ns8')
    request = factory.PollForData(
        Header={
            'Identification': uuid.uuid4(),
            'DocumentType': {
                '_value_1': DOCUMENT_TYPE_UN_CEFACT.QUERY.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.UN_CEFACT.value,
            },
            'Creation': f'{datetime.utcnow().strftime(TIME_FORMAT)}',
            'PhysicalSenderEnergyParty': {
                'Identification': {
                    '_value_1': third_party_gsn,
                    'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value,
                }
            },
            'JuridicalSenderEnergyParty': {
                'Identification': {
                    '_value_1': third_party_gsn,
                    'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value,
                }
            },
            'JuridicalRecipientEnergyParty': {
                'Identification': {'_value_1': ELHUB_GSN, 'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value}
            },
        },
        ProcessEnergyContext={
            'EnergyBusinessProcess': {'_value_1': 'POLL', 'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.ELHUB.value},
            'EnergyBusinessProcessRole': {
                '_value_1': 'DDQ',
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.UN_CEFACT.value,
            },
            'EnergyIndustryClassification': "23",
        },
        Payload={},
    )
    try:
        response = client.service.PollForData(request)
        if "ResultDataSet" in response:
            xml_response = ET.tostring(history.last_received["envelope"], encoding="unicode")
            return xml_response
        else:
            logger.error(f"Unknown response: {response}")
    except zeep.exceptions.Fault as ex:
        logger.error(f"Bad response: {ex}")

    return None
