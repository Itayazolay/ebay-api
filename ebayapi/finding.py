from lxml import etree, objectify

from ebayapi import API, EbayError, Request
from ebayapi.parse import dict2xml

EM = objectify.ElementMaker(annotate=False)


class FindingAPI(API):
    def headers(self, call_name):
        headers = {}
        headers.update({
            "X-EBAY-SOA-OPERATION-NAME": call_name,
            "X-EBAY-SOA-SECURITY-APPNAME": self.app_id,
            "X-EBAY-SOA-SERVICE-VERSION": str(self.version),
            "X-EBAY-SOA-RESPONSE-DATA-FORMAT": "XML",
            "X-EBAY-SOA-REQUEST-DATA-FORMAT": "XML"
        })
        return headers

    def parse(self, response):
        response = super().parse(response)
        if response.get('error'):
            raise EbayError(response['error']['message'],
                            errors=response['error'])
        if response.get('Ack') == "Failure":
            raise EbayError(response['Errors']['ErrorClassification'],
                            errors=response['Errors'])
        return response

    @property
    def url(self):
        return "http://svcs.ebay.com/services/search/FindingService/v1"

    def request(self, call_name, data):
        """
        Create an API Request.

        :param str call_name: Api call name. Adding `Request` in the xml schema.
        :param dict data: The api request data to send.
        :return: Request to send to ebay servers.
        :rtype: urllib.Request
        """
        call_req = getattr(EM, "{call_name}Request".format(call_name=call_name))(
            xmlns="http://www.ebay.com/marketplace/search/v1/services")
        xml = dict2xml(call_req, data)
        data = etree.tostring(xml, encoding="UTF-8", xml_declaration=True,
                              pretty_print=True)
        return Request(method="POST", url=self.url, data=data,
                       headers=self.headers(call_name))
