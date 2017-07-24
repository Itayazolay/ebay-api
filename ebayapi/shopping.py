from lxml import objectify

from ebayapi import API, EbayError

EM = objectify.ElementMaker(annotate=False)


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
            "X-EBAY-API-VERSION": str(self.version),
            "X-EBAY-API-REQUEST-ENCODING": "XML"
        })
        return headers

    def parse(self, response) -> dict:
        response = super().parse(response)
        if response['Ack'] == "Failure":
            raise EbayError(response['Errors']['ErrorClassification'], errors=response['Errors'])
        return response