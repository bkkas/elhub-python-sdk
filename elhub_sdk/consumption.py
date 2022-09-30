from typing import Optional

import uuid
from datetime import datetime

from elhub_sdk.client import APIClient
from elhub_sdk.constants import ELHUB_GSN, TIME_FORMAT
from elhub_sdk.enums import SCHEME_AGENCY_IDENTIFIER, LIST_AGENCY_IDENTIFIER, DOCUMENT_TYPE_EBIX, BSR_IDS, ROLES, \
    QUERY_MARKET, WSDL_FILES


def request_consumption(meter_identificator:str, third_party_gsn: str, start: datetime, end: datetime)->Optional[dict]:
    """

    Args:
        meter_identificator:
        third_party_gsn:
        start:
        end:

    Returns:

    """
    client = APIClient.get_zeep_client(wsdl=WSDL_FILES.QUERY.value)

    factory = client.type_factory('ns4')
    eh_request = factory.RequestDataFromElhub(
        Header={
            'Identification': uuid.uuid4(),
            'DocumentType': {'_value_1': DOCUMENT_TYPE_EBIX.METERING_DATA.value,
                             'listAgencyIdentifier': LIST_AGENCY_IDENTIFIER.EBIX.value},
            'Creation': f'{datetime.utcnow().strftime(TIME_FORMAT)}',
            'PhysicalSenderEnergyParty': {
                'Identification': {'_value_1': third_party_gsn, 'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value}},
            'JuridicalSenderEnergyParty': {
                'Identification': {'_value_1': third_party_gsn, 'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value}},
            'JuridicalRecipientEnergyParty': {'Identification':
                                                  {'_value_1': ELHUB_GSN,
                                                   'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value}},
        },
        ProcessEnergyContext={  # https://dok.elhub.no/ediel200utkast/general#General-Process
            'EnergyBusinessProcess': {'_value_1': BSR_IDS.METERING_VALUES.value, 'listAgencyIdentifier': "89"},
            'EnergyBusinessProcessRole': {'_value_1': ROLES.THIRD_PARTY.value, 'listAgencyIdentifier': "6"},
            'EnergyIndustryClassification': "23"
        },
        PayloadMPEvent={
            'QueryTypeCode': QUERY_MARKET.METERING_VALUES_TIME_SERIES.value,
            'Period': {
                'Start': f'{start.strftime(TIME_FORMAT)}',
                'End': f'{end.strftime(TIME_FORMAT)}'
            },
            'MeteringPointUsedDomainLocation': {
                'Identification': {
                    '_value_1': meter_identificator,
                    'schemeAgencyIdentifier': SCHEME_AGENCY_IDENTIFIER.GS1.value
                }
            }
        }
    )

    response = client.service.RequestDataFromElhub(eh_request)
    return response
