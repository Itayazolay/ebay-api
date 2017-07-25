"""
Api base request.
"""

from lxml import objectify, etree

from ebayapi.parse import dict2xml, xml2dict

EM = objectify.ElementMaker(annotate=False)


class EbayError(Exception):
    def __init__(self, *args, errors=None):
        super().__init__(*args)
        self.errors = errors


class Request:
    def __init__(self, method, url, headers, params=None, data=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        self.params = params


class API:
    """Base API implementations for ebay api."""

    def __init__(self, app_id, version, **config):
        self.app_id = app_id
        self.version = version
        self.config = config
        self.url = ""

    def headers(self, call_name):
        """
        Return Request headers for the request call.

        :param call_name: Name of the api call.
        :return: Request headers.
        :rtype: dict
        """
        return {
            "X-EBAY-API-APP-ID": self.app_id,
            "X-EBAY-API-CALL-NAME": call_name,
            # "X-EBAY-API-SITE-ID": self.config['siteid'],
        }

    def request(self, call_name, data):
        """
        Create an API Request.

        :param str call_name: Api call name. Adding `Request` in the xml schema.
        :param dict data: The api request data to send.
        :return: Request to send to ebay servers.
        :rtype: Request
        """
        call_req = getattr(EM, "{call_name}Request".format(call_name=call_name))(
            xmlns="urn:ebay:apis:eBLBaseComponents")
        xml = dict2xml(call_req, data)
        data = etree.tostring(xml, encoding="UTF-8", xml_declaration=True,
                              pretty_print=True)
        return Request(method="POST", url=self.url, data=data,
                       headers=self.headers(call_name))

    def parse(self, response) -> dict:
        """
        Parse api response data.

        :param response: Response text from ebay.
        :return: Response data as dict.
        :rtype: dict
        """
        response = objectify.fromstring(response)
        return xml2dict(response)
