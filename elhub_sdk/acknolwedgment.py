"""
Acknowledgement related functions


After the market party has persisted the received messages,
an Acknowledgement message referring to the polled data set
must be sent back to Elhub on the polling service to confirm
that the messages has been received.

Note: Elhub will send a 200 response regardless of the validity of the
Original Business Document Reference. To confirm that the
acknowlegment was sucessfull poll again and check if the
request have been acknowledged.

"""

import logging
import uuid
from datetime import datetime
from typing import Optional, Literal

import zeep
from zeep.plugins import HistoryPlugin

from elhub_sdk.constants import ELHUB_GSN, TIME_FORMAT
from elhub_sdk.enums import (
    BSR_IDS,
    DOCUMENT_TYPE_UN_CEFACT,
    LIST_AGENCY_IDENTIFIER,
    ROLES,
    SCHEME_AGENCY_IDENTIFIER,
    STATUS_TYPE,
)

logger = logging.getLogger()


def acknowledge_poll(
    client: zeep.Client,
    history: HistoryPlugin,
    sender_gsn: str,
    original_business_document_reference: str,
    process_role: ROLES = ROLES.THIRD_PARTY,
) -> bool:
    """
    Metering Values | Market processes WSDL
    Args:
        history:
        client:
        meter_identificator:
        sender_gsn:
        original_business_document_reference:
        process_role:

    Returns:

    """

    factory = client.type_factory('ns7')
    eh_request = factory.Acknowledgement(
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
        ProcessEnergyContext={  # https://dok.elhub.no/ediel2/general#General-Process
            'EnergyBusinessProcess': {
                '_value_1': BSR_IDS.POLL.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.ELHUB.value,
            },
            'EnergyBusinessProcessRole': {
                '_value_1': process_role.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.UN_CEFACT.value,
            },
            'EnergyIndustryClassification': "23",
        },
        PayloadResponseEvent={
            'StatusType': {
                '_value_1': STATUS_TYPE.ACCEPTED.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.UN_CEFACT.value,
            },
            'OriginalBusinessDocumentReference': original_business_document_reference,
        },
    )

    try:
        response = client.service.AcknowledgePoll(eh_request)
        if history.last_received:
            return True
        logger.error(f"Unknown error: {response}")
    except Exception as ex:
        logger.exception(ex)
    return False
