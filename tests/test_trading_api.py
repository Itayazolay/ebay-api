import os

import pytest
import requests
import yaml

from ebayapi import TradingAPI, EbayError


@pytest.fixture
def config():
    """Get config fixture."""
    conf = os.environ.get("EBAY_CONF", "ebay-conf.yaml")
    config = yaml.load(open(conf))
    return config['api.ebay.com']


@pytest.fixture
def api(config):
    """Get Trading API instance."""
    return TradingAPI(config['appid'], config['version'], config['siteid'])


def test_get_item_transactions(api, config):
    """Test valid GetItemTransactions request."""
    request = api.request("GetItemTransactions", {
        "RequesterCredentials": {
            "eBayAuthToken": config['token']
        },
        "ItemID": 1
    })
    response = requests.request(request.method, request.url,
                                headers=request.headers, data=request.data)
    assert response.status_code == 200
    try:
        api.parse(response.content)
    except EbayError as err:
        errors = getattr(err, "errors")
        assert isinstance(errors, dict)
