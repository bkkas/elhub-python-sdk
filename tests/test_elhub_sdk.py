"""
Tests for `elhub_sdk` package.
"""

import datetime
from pprint import pprint

from elhub_sdk.consumption import request_consumption, poll_consumption
from elhub_sdk.settings import THIRD_PARTY_GSN
import logging
logger = logging.getLogger(__name__)


def test_request_consumption():
    """
    Requesting consumption for a meter
    Returns:

    """
    meter_identificator = "707057500057411768"
    start = datetime.datetime.now() - datetime.timedelta(days=30)
    end = start+datetime.timedelta(days=1)

    response = request_consumption(
        meter_identificator,
        third_party_gsn = THIRD_PARTY_GSN,
        start=start,
        end=end)

    assert response == None


def test_poll_consumption():
    """
    Pooling data from Elhub
    Returns:

    """
    response = poll_consumption(THIRD_PARTY_GSN)
    assert response


