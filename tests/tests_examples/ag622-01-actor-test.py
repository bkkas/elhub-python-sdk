import logging

from elhub_sdk.client import APIClient
from elhub_sdk.consumption import poll_consumption
from elhub_sdk.enums import THIRD_PARTY_ACTION
from elhub_sdk.settings import CERT_FILE, KEY_FILE, WSDL_FILES_CONFIG_TEST
from elhub_sdk.third_party import request_action
from tests.tests_examples.config import TEST_METER_IDENTIFICATORS, THIRD_PARTY_GSN_EXA

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)


METER_IDENTIFICATOR = TEST_METER_IDENTIFICATORS["profiled"][1]


def update_third_party():
    logger.info("Adding profiled meter as third party")
    client, history = APIClient.get_zeep_client(
        wsdl=WSDL_FILES_CONFIG_TEST['MARKET_PROCESSES'], secure=True, key_file=KEY_FILE, cert_file=CERT_FILE
    )
    response = request_action(
        client, history, THIRD_PARTY_GSN_EXA, meter_identificator=METER_IDENTIFICATOR, action=THIRD_PARTY_ACTION.ADD
    )
    return response


def get_consumption():
    """
    Pooling data from Elhub
    Returns:

    """
    logger.debug("Getting consumption...")
    client, history = APIClient.get_zeep_client(
        wsdl=WSDL_FILES_CONFIG_TEST['POOL_METERING'], secure=True, key_file=KEY_FILE, cert_file=CERT_FILE
    )

    response = poll_consumption(client, history, THIRD_PARTY_GSN_EXA)
    return response


def remove_third_party():
    """

    Returns:

    """
    client, history = APIClient.get_zeep_client(
        wsdl=WSDL_FILES_CONFIG_TEST['MARKET_PROCESSES'], secure=True, key_file=KEY_FILE, cert_file=CERT_FILE
    )

    response = request_action(
        client, history, THIRD_PARTY_GSN_EXA, meter_identificator=METER_IDENTIFICATOR, action=THIRD_PARTY_ACTION.DELETE
    )
    return response


if __name__ == "__main__":
    logger.debug(f"Initiating tests with identificator: {METER_IDENTIFICATOR}")
    # response = update_third_party()
    # print(response)

    # response = get_consumption()
    # print(response)

    response = remove_third_party()
    # print(response)
