import datetime
import logging

import pytest

from elhub_sdk.client import APIClient
from elhub_sdk.consumption import poll_consumption, request_consumption
from elhub_sdk.enums import THIRD_PARTY_ACTION
from elhub_sdk.settings import CERT_FILE, KEY_FILE, WSDL_FILES_CONFIG_TEST
from elhub_sdk.third_party import request_action
from tests.tests_examples.config import THIRD_PARTY_GSN_EXA

logger = logging.getLogger(__name__)


@pytest.mark.integrationtest
def test_third_party_delete():
    """
    Tests the addition of a third party against Exa2
    Returns:

    """
    client, history = APIClient.get_zeep_client(
        wsdl=WSDL_FILES_CONFIG_TEST['MARKET_PROCESSES'], secure=True, key_file=KEY_FILE, cert_file=CERT_FILE
    )
    meter_identificator = "707057500084111792"
    response = request_action(
        client, history, THIRD_PARTY_GSN_EXA, meter_identificator=meter_identificator, action=THIRD_PARTY_ACTION.DELETE
    )
    assert response


@pytest.mark.integrationtest
def test_third_party_add():
    """
    Tests the addition of a third party against Exa2
    Returns:

    """
    client, history = APIClient.get_zeep_client(
        wsdl=WSDL_FILES_CONFIG_TEST['MARKET_PROCESSES'], secure=True, key_file=KEY_FILE, cert_file=CERT_FILE
    )
    meter_identificator = "707057500084111792"
    response = request_action(
        client, history, THIRD_PARTY_GSN_EXA, meter_identificator=meter_identificator, action=THIRD_PARTY_ACTION.ADD
    )
    assert response


@pytest.mark.integrationtest
def test_poll_consumption():
    """
    Pooling data from Elhub
    Returns:

    """
    client, history = APIClient.get_zeep_client(
        wsdl=WSDL_FILES_CONFIG_TEST['POOL_METERING'], secure=True, key_file=KEY_FILE, cert_file=CERT_FILE
    )

    response = poll_consumption(client, history, THIRD_PARTY_GSN_EXA)
    assert response


@pytest.mark.integrationtest
def test_request_consumption():
    """
    Query requesting consumption for a meter
    Returns:

    """
    meter_identificator = "707057500057411768"
    start = datetime.datetime(2022, 5, 1)
    end = start + datetime.timedelta(days=7)

    client, history = APIClient.get_zeep_client(
        wsdl=WSDL_FILES_CONFIG_TEST['QUERY'], secure=True, key_file=KEY_FILE, cert_file=CERT_FILE
    )

    response = request_consumption(
        client, history, meter_identificator, sender_gsn=THIRD_PARTY_GSN_EXA, start=start, end=end
    )
    assert response
