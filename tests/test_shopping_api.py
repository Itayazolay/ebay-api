import os

import pytest
import requests
import yaml

from ebayapi import ShoppingAPI


@pytest.fixture
def config():
    """Get config fixture."""
    conf = os.environ.get("EBAY_CONF", "ebay-conf.yaml")
    config = yaml.load(open(conf))
    return config['open.api.ebay.com']


@pytest.fixture
def api(config):
    """Get Trading API instance."""
    return ShoppingAPI(config['appid'], config['version'])


def test_get_multiple_items(api):
    """Test get multiple items request."""
    items = [292188846779, 292187436212]
    req = api.request("GetMultipleItems", {"ItemID": items})
    response = requests.request(req.method, req.url, headers=req.headers, data=req.data, params=req.params)
    response = api.parse(response.content)
    assert len(response.get("Item", [])) > 0
    assert [i['ItemID'] for i in response['Item']] == items
