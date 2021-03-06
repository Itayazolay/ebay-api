from collections import OrderedDict

import pytest
from lxml import objectify
from lxml.etree import tostring

from ebayapi.parse import dict2xml, xml2dict


@pytest.fixture(scope="session")
def samples():
    """return equivalent dict and xml."""
    sample = OrderedDict((("a", {"a1": "a2"}),
                         ("b", ["b1", "b2", "b3"]),
                         ("c", 5)))
    xml_sample = b'<Sample>\n' \
                 b'  <a>\n' \
                 b'    <a1>a2</a1>\n' \
                 b'  </a>\n' \
                 b'  <b>b1</b>\n' \
                 b'  <b>b2</b>\n' \
                 b'  <b>b3</b>\n' \
                 b'  <c>5</c>\n' \
                 b'</Sample>\n'
    return sample, xml_sample


def test_simple_dict2xml(samples):
    """Test simple dict2xml conversion."""
    sample, xml_sample = samples
    tree = dict2xml(objectify.ElementMaker(annotate=False).Sample(), sample)
    assert tostring(tree, pretty_print=True) == xml_sample


def test_simple_xml2dict(samples):
    """Test simple xml2dict conversion."""
    sample, xml_sample = samples
    element = objectify.fromstring(xml_sample)
    data = xml2dict(element)
    assert data == sample
