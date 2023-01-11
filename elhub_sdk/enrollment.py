"""
Processes related to the enrollment of customers
"""
import logging
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional

import zeep

from elhub_sdk.constants import ELHUB_GSN, TIME_FORMAT
from elhub_sdk.enums import BSR_IDS, DOCUMENT_TYPE_EBIX, LIST_AGENCY_IDENTIFIER, ROLES, SCHEME_AGENCY_IDENTIFIER

logger = logging.getLogger()


def get_meter_characteristics(
    client: zeep.Client,
    history: zeep.plugins.HistoryPlugin,
    meter_identificator: str,
    sender_gsn: str,
    process_role: ROLES = ROLES.THIRD_PARTY,
) -> Optional[str]:
    """
    https://dok.elhub.no/ediel200utkast/requestupfrontmeteringpointcharacteristics
    Args:
        client: zeep client
        history: zeep history
        meter_identificator: meter identificator
        sender_gsn: sender gsn
        process_role: process role

    Returns:

    """

    factory = client.type_factory('ns1')
    eh_request = factory.RequestUpfrontMeteringPointCharacteristics(
        Header={
            'Identification': uuid.uuid4(),
            'DocumentType': {
                '_value_1': DOCUMENT_TYPE_EBIX.CHANGE_DATA.value,
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
                '_value_1': BSR_IDS.METERING_POINT_CHARACTERISTICS.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.ELHUB.value,
            },
            'EnergyBusinessProcessRole': {
                '_value_1': process_role.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.UN_CEFACT.value,
            },
            'EnergyIndustryClassification': "23",
        },
        PayloadMPEvent={
            'MeteringPointUsedDomainLocation': {
                'Identification': {
                    '_value_1': meter_identificator,
                    'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value,
                }
            },
        },
    )

    try:
        response = client.service.RequestUpfrontMeteringPointCharacteristics(eh_request)
        if history.last_received and "ResponseUpfrontMeteringPointCharacteristics" in response:
            xml_response = ET.tostring(history.last_received["envelope"], encoding="unicode")
            return xml_response
        logger.error(f"Unknown error: {response}")
    except Exception as ex:
        logger.exception(ex)

    return None
