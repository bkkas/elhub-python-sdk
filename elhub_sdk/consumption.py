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
from zeep.plugins import HistoryPlugin

from elhub_sdk.constants import ELHUB_GSN, TIME_FORMAT
from elhub_sdk.enums import (
    BSR_IDS,
    DOCUMENT_TYPE_EBIX,
    DOCUMENT_TYPE_UN_CEFACT,
    ENERGY_INDUSTRY_CLASSIFICATION,
    LIST_AGENCY_IDENTIFIER,
    QUERY_MARKET,
    ROLES,
    SCHEME_AGENCY_IDENTIFIER,
)

logger = logging.getLogger()


def request_consumption(
    client: zeep.Client,
    history: HistoryPlugin,
    meter_identificator: str,
    sender_gsn: str,
    start: datetime,
    end: datetime,
    process_role: ROLES = ROLES.THIRD_PARTY,
) -> bool:
    """
    Query WSDL
    Args:
        history:
        client:
        meter_identificator:
        sender_gsn:
        start:
        end:
        process_role:

    Returns:

    """

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
                    '_value_1': sender_gsn,
                    'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value,
                }
            },
            'JuridicalSenderEnergyParty': {
                'Identification': {
                    '_value_1': sender_gsn,
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
                '_value_1': process_role.value,
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

    try:
        response = client.service.RequestDataFromElhub(eh_request)
        if history.last_received:
            return True
        logger.error(f"Unknown error: {response}")
    except Exception as ex:
        logger.exception(ex)
    return False


def poll_consumption(
    client: zeep.Client, history: HistoryPlugin, sender_gsn: str, process_role: ROLES = ROLES.THIRD_PARTY
) -> Optional[str]:
    """
    Poll WSDL
    Args:
        client:
        history:
        sender_gsn:
        process_role:

    Returns:

    """

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
                    '_value_1': sender_gsn,
                    'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value,
                }
            },
            'JuridicalSenderEnergyParty': {
                'Identification': {
                    '_value_1': sender_gsn,
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
                '_value_1': process_role.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.UN_CEFACT.value,
            },
            'EnergyIndustryClassification': ENERGY_INDUSTRY_CLASSIFICATION.ELECTRICITY_SUPPLY.value,
        },
        Payload={},
    )
    try:
        response = client.service.PollForData(request)
        if "ResultDataSet" in response and history.last_received:
            xml_response = ET.tostring(history.last_received["envelope"], encoding="unicode")
            return xml_response
        logger.error(f"Unknown response: {response}")
    except zeep.exceptions.Fault as ex:
        logger.error(f"Bad response: {ex}")

    return None
