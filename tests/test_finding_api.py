import os

import pytest
import requests
import yaml

from ebayapi import FindingAPI, Request


@pytest.fixture
def config():
    """Get config fixture."""
    conf = os.environ.get("EBAY_CONF", "ebay-conf.yaml")
    config = yaml.load(open(conf))
    return config['svcs.ebay.com']


@pytest.fixture
def api(config):
    """Get Trading API instance."""
    api = FindingAPI(config['appid'], config['version'])
    api.url = "http://svcs.sandbox.ebay.com/services/search/FindingService/v1"
    return api


def test_find_by_keywords(api):
    """Send sample find items by keywords request"""
    req = api.request("findItemsByKeywords", {
        "keywords": "Iphone 6 plus",
        "paginationInput": {"entriesPerPage": 100}
    })  # type: Request
    response = requests.request(req.method, req.url, headers=req.headers, data=req.data, params=req.params)
    response = api.parse(response.content)
    assert response.get('searchResult')
    assert len(response.get('searchResult', {}).get("item", [])) > 0
