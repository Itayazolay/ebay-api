"""
Api base request.
"""
from urllib.request import Request
from lxml import objectify, etree

EM = objectify.ElementMaker(annotate=False)


class EbayError(Exception):
    def __init__(self, *args, errors=None) -> None:
        super().__init__(*args)
        self.errors = errors


class API:
    def __init__(self, config):
        self.config = config

    @property
    def url(self) -> str:
        pass

    def headers(self, call_name):
        return {
            "X-EBAY-API-APP-ID": self.config['appid'],
            "X-EBAY-API-CALL-NAME": call_name,
            # "X-EBAY-API-SITE-ID": self.config['siteid'],
        }

    def request(self, call_name, data) -> Request:
        call_req = getattr(EM, f"{call_name}Request")(
            xmlns="urn:ebay:apis:eBLBaseComponents")
        xml = dict2xml(call_req, data)
        data = etree.tostring(xml, encoding="UTF-8", xml_declaration=True,
                              pretty_print=True)
        return Request(method="POST", url=self.url, data=data,
                       headers=self.headers(call_name))

    def parse(self, response) -> dict:
        response = objectify.fromstring(response)
        return xml2dict(response)


def dict2xml(root: objectify.Element, data: dict):
    for key, value in data.items():
        if isinstance(value, dict):
            sub_root = getattr(EM, key)()
            element = dict2xml(sub_root, value)
            root.append(element)
        elif isinstance(value, list):
            """
            {"a": ["b","c","d"]} => <a>b</a> <a>c</a> <a>d</a>
            {"a": [{"b":1}, {"b": 2}] } => <a><b>1</b></a> <a><b>2</b></a>
            """
            sub_root = getattr(EM, key)
            for val in value:
                if isinstance(val, dict):
                    element = dict2xml(sub_root(), val)
                else:
                    element = sub_root(val)
                root.append(element)
        else:
            element = getattr(EM, key)(value)
            root.append(element)
    return root


def xml2dict(root: objectify.Element):
    data = {}
    namespace = root.nsmap.get(None, "")
    clean_tag = lambda tag: tag.replace("{%s}" % namespace, "")

    for element in root.getchildren():
        # Figure out type
        if not hasattr(element, "pyval"):  # A root element
            sub_data = xml2dict(element)
            name, val = clean_tag(element.tag), sub_data
        else:
            name, val = clean_tag(element.tag), element.pyval
        # Add the value to the data dict
        if name in data:
            # If it's already in data, append or make a list out of it.
            if isinstance(data[name], list):
                data[name].append(val)
            else:
                data[name] = [data[name], val]
        else:
            # Just a regular value.
            data[name] = val
    return data


class TradingAPI(API):
    """Trading API Request Implementation."""

    @property
    def url(self) -> str:
        return "https://api.ebay.com/ws/api.dll"

    def headers(self, call_name: str) -> dict:
        headers = super(TradingAPI, self).headers(call_name)
        headers.update({
            "X-EBAY-API-COMPATIBILITY-LEVEL": str(self.config['version']),
            "X-EBAY-API-SITEID": str(self.config['siteid']),
            "Content-Type": "text/xml",
        })
        return headers

    def parse(self, response) -> dict:
        response = super().parse(response)
        if response['Ack'] == "Failure":
            raise EbayError(response['Errors']['ErrorClassification'],
                            errors=response['Errors'])
        return response


class ShoppingAPI(API):
    """
    Shopping API Request implementation.
    """

    @property
    def url(self) -> str:
        return "http://open.api.ebay.com/shopping"

    def headers(self, call_name: str) -> dict:
        headers = super(ShoppingAPI, self).headers(call_name)
        headers.update({
            "X-EBAY-API-VERSION": str(self.config['version']),
            "X-EBAY-API-REQUEST-ENCODING": "XML"
        })
        return headers
