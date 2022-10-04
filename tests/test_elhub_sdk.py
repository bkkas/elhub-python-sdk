"""
Tests for `elhub_sdk` package.
These are meant to be run against a SOAPUI instance, they don't use security
"""

import datetime
import logging

import pytest

from elhub_sdk.client import APIClient
from elhub_sdk.consumption import poll_consumption, request_consumption
from elhub_sdk.settings import WSDL_FILES_CONFIG

logger = logging.getLogger(__name__)

# Third party GSN
THIRD_PARTY_GSN = "123456789"


def test_dummy():
    """
    This is needed for pytest to return 0 on exit, most of the tests are marked
    as integration
    Returns:

    """
    assert True


@pytest.mark.integrationtest
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


@pytest.mark.integrationtest
def test_poll_consumption():
    """
    Pooling data from Elhub
    Returns:

    """
    client, history = APIClient.get_zeep_client(wsdl=WSDL_FILES_CONFIG['POOL_METERING'], secure=False)
    response = poll_consumption(client, history, THIRD_PARTY_GSN)
    assert response
