from lxml import objectify

from ebayapi import API, EbayError

EM = objectify.ElementMaker(annotate=False)


class TradingAPI(API):
    """Trading API Request Implementation."""

    def __init__(self, app_id, version, site_id, **config):
        super().__init__(app_id, version, **config)
        self.site_id = site_id

    @property
    def url(self) -> str:
        return "https://api.ebay.com/ws/api.dll"

    def headers(self, call_name: str) -> dict:
        headers = super(TradingAPI, self).headers(call_name)
        headers.update({
            "X-EBAY-API-COMPATIBILITY-LEVEL": str(self.version),
            "X-EBAY-API-SITEID": str(self.site_id),
            "Content-Type": "text/xml",
        })
        return headers

    def parse(self, response) -> dict:
        response = super().parse(response)
        if response['Ack'] == "Failure":
            raise EbayError(response['Errors']['ErrorClassification'],
                            errors=response['Errors'])
        return response
