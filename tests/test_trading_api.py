import os
import yaml
import pytest
from ebayapi import TradingAPI, EbayError
import requests


@pytest.fixture
def config():
    conf = os.environ.get("EBAY_CONF", "ebay-conf.yaml")
    config = yaml.load(open(conf))
    return config['api.ebay.com']


@pytest.fixture
def api(config):
    return TradingAPI(config)


def test_valid_request(api: TradingAPI):
    request = api.request("GetItemTransactions", {
        "RequesterCredentials": {
            "eBayAuthToken": api.config['token']
        },
        "ItemID": 1
    })
    response = requests.request(request.method, request.full_url,
                                headers=request.headers, data=request.data)
    assert response.status_code == 200
    try:
        api.parse(response.content)
    except EbayError as err:
        errors = getattr(err, "errors")
        assert isinstance(errors, dict)
