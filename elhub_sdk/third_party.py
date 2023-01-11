"""
Manages third party requests

It mainly uses the endpoint UpdateThirdPartyAccessRequest

ns7:UpdateThirdPartyAccess(Header: ns2:Elhub_HeaderType, ProcessEnergyContext: ns2:Elhub_EnergyContextType,
    PayloadMPEvent: ns2:Elhub_UpdateThirdPartyAccessType)

ns2: Elhub_UpdateThirdPartyAccessType(
    UpdateIndicator: ns3: AddDeleteUpdate, MeteringPointUsedDomainLocation: ns2:Elhub_MeteringPointType,
    ConsumerInvolvedCustomerParty: ns2:Elhub_EndUserType)

<xsd:simpleType name="AddDeleteUpdate">
    <xsd:restriction base="xsd:string">
        <xsd:enumeration value="Add"/>
        <xsd:enumeration value="Delete"/>
        <xsd:enumeration value="Update"/>
    </xsd:restriction>
</xsd:simpleType>

"""
import logging
import uuid
from datetime import datetime
from typing import Any, Dict

import zeep

from elhub_sdk.constants import ELHUB_GSN, TIME_FORMAT
from elhub_sdk.enums import (
    BSR_IDS,
    DOCUMENT_TYPE_EBIX,
    LIST_AGENCY_IDENTIFIER,
    ROLES,
    SCHEME_AGENCY_IDENTIFIER,
    THIRD_PARTY_ACTION,
)

logger = logging.getLogger()


def request_action(
    client: zeep.Client,
    history: zeep.plugins.HistoryPlugin,
    sender_gsn: str,
    meter_identificator: str,
    action: THIRD_PARTY_ACTION,
    extended_storage=False,
):
    """

    Args:
        history: zeep history
        client: zeep client
        sender_gsn: sender gsn
        meter_identificator: meter identificator
        action: action to perform
        extended_storage: extended storage
    Returns:

    """

    factory = client.type_factory('ns7')

    playload_event: Dict[str, Any] = {
        'UpdateIndicator': action.value,
        'MeteringPointUsedDomainLocation': {
            'Identification': {
                '_value_1': meter_identificator,
                'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value,
            }
        },
    }

    if extended_storage:
        playload_event['ConsumerInvolvedCustomerParty'] = {'ExtendedStorageMeteringValues': "true"}

    eh_request = factory.UpdateThirdPartyAccess(
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
                '_value_1': BSR_IDS.THIRD_PARTY.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.ELHUB.value,
            },
            'EnergyBusinessProcessRole': {
                '_value_1': ROLES.THIRD_PARTY.value,
                'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.UN_CEFACT.value,
            },
            'EnergyIndustryClassification': "23",
        },
        PayloadMPEvent=playload_event,
    )

    try:
        response = client.service.UpdateThirdPartyAccess(eh_request)
        return response
    except Exception as ex:
        logger.exception(ex)
    return False
