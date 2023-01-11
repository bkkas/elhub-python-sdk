import logging

from elhub_sdk.client import APIClient
from elhub_sdk.enrollment import get_meter_characteristics
from elhub_sdk.settings import CERT_FILE, KEY_FILE, WSDL_FILES_CONFIG_TEST
from tests.tests_examples.config import TEST_METER_IDENTIFICATORS, VOLTE_GSN_EXA

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


METER_IDENTIFICATOR = TEST_METER_IDENTIFICATORS["profiled"][0]


def meter_characteristics():
    client, history = APIClient.get_zeep_client(
        wsdl=WSDL_FILES_CONFIG_TEST['QUERY'], secure=True, key_file=KEY_FILE, cert_file=CERT_FILE
    )
    response = get_meter_characteristics(
        client=client, history=history, meter_identificator=METER_IDENTIFICATOR, sender_gsn=VOLTE_GSN_EXA
    )
    return response


if __name__ == "__main__":
    logger.debug(f"Initiating tests with identificator: {METER_IDENTIFICATOR}")
    response = meter_characteristics()
    print(response)
