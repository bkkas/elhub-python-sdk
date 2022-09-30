#!/usr/bin/env python
"""Tests for `elhub_sdk` package."""
import datetime

import pytest

from elhub_sdk.client import APIClient
from elhub_sdk.consumption import request_consumption


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    del response


def test_consumption_query():
    meter_identificator = "707057500010503271"
    VOLTE_3RD_PARTY_GSN = "7080004168879"
    start = datetime.datetime.now() - datetime.timedelta(days=30)
    end = start+datetime.timedelta(days=1)

    response = request_consumption(
        meter_identificator,
        third_party_gsn = VOLTE_3RD_PARTY_GSN,
        start=start,
        end=end)
