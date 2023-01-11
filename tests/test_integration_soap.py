"""
Tests for `elhub_sdk` package.
These are meant to be run against a SOAPUI instance, they don't use security
"""

import datetime
import logging

import pytest

from elhub_sdk.client import APIClient
from elhub_sdk.consumption import poll_consumption, request_consumption
from elhub_sdk.enrollment import get_meter_characteristics
from elhub_sdk.enums import THIRD_PARTY_ACTION
from elhub_sdk.settings import WSDL_FILES_CONFIG
from elhub_sdk.third_party import request_action
from tests.tests_examples.config import THIRD_PARTY_GSN

logger = logging.getLogger(__name__)


def test_dummy():
    """
    This is needed for pytest to return 0 on exit, most of the tests are marked
    as integration
    Returns:

    """
    assert True


@pytest.mark.soapuitest
def test_request_consumption():
    """
    Query requesting consumption for a meter
    Returns:

    """
    meter_identificator = "807057500057411761"
    start = datetime.datetime.now() - datetime.timedelta(days=30)
    end = start + datetime.timedelta(days=1)

    client, history = APIClient.get_zeep_client(wsdl=WSDL_FILES_CONFIG['QUERY'], secure=False)

    response = request_consumption(
        client, history, meter_identificator, sender_gsn=THIRD_PARTY_GSN, start=start, end=end
    )

    assert response


@pytest.mark.soapuitest
def test_poll_consumption():
    """
    Pooling data from Elhub
    Returns:

    """
    client, history = APIClient.get_zeep_client(wsdl=WSDL_FILES_CONFIG['POOL_METERING'], secure=False)
    response = poll_consumption(client, history, THIRD_PARTY_GSN)
    assert response


@pytest.mark.soapuitest
def test_third_party_add():
    """
    Tests the addition of a third party
    Returns:

    """
    client, history = APIClient.get_zeep_client(wsdl=WSDL_FILES_CONFIG['MARKET_PROCESSES'], secure=False)
    meter_identificator = "807057500057411761"
    response = request_action(
        client, history, THIRD_PARTY_GSN, meter_identificator=meter_identificator, action=THIRD_PARTY_ACTION.ADD
    )
    assert response


@pytest.mark.soapuitest
def test_third_party_add_extended():
    """
    Tests the addition of a third party with extended storage
    Returns:

    """
    client, history = APIClient.get_zeep_client(wsdl=WSDL_FILES_CONFIG['MARKET_PROCESSES'], secure=False)
    meter_identificator = "807057500057411761"
    response = request_action(
        client, history, THIRD_PARTY_GSN, meter_identificator=meter_identificator, action=THIRD_PARTY_ACTION.ADD
    )
    assert response


@pytest.mark.soapuitest
def test_third_party_update_extended():
    """
    Tests the update of a third party with extended storage
    Returns:

    """
    client, history = APIClient.get_zeep_client(wsdl=WSDL_FILES_CONFIG['MARKET_PROCESSES'], secure=False)
    meter_identificator = "807057500057411761"
    response = request_action(
        client,
        history,
        THIRD_PARTY_GSN,
        meter_identificator=meter_identificator,
        action=THIRD_PARTY_ACTION.UPDATE,
        extended_storage=True,
    )
    assert response


@pytest.mark.soapuitest
def test_third_party_delete():
    """
    Tests the deletion of a third party with extended storage
    Returns:

    """
    client, history = APIClient.get_zeep_client(wsdl=WSDL_FILES_CONFIG['MARKET_PROCESSES'], secure=False)
    meter_identificator = "807057500057411761"
    response = request_action(
        client, history, THIRD_PARTY_GSN, meter_identificator=meter_identificator, action=THIRD_PARTY_ACTION.DELETE
    )
    assert response


@pytest.mark.soapuitest
def test_get_meter_characteristics():
    client, history = APIClient.get_zeep_client(wsdl=WSDL_FILES_CONFIG['QUERY'], secure=False)
    meter_identificator = "707057500022939815"
    response = get_meter_characteristics(
        client=client, history=history, meter_identificator=meter_identificator, sender_gsn=THIRD_PARTY_GSN
    )
    assert response
