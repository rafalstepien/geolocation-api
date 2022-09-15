import json

import requests

from config_loader.config_loader import config
from ipstack.constants import IPSTACK_BASE_URL
from ipstack.models import IpstackStandardLookupResponseModel


class IpstackClient:
    def __init__(self):
        pass

    def get_data_for_ip_address(self, ip_address: str):
        response = requests.get(f"{IPSTACK_BASE_URL}{ip_address}?access_key={config.IPSTACK_ACCESS_KEY}")
        return self._parse_upstream_response(response)

    @staticmethod
    def _parse_upstream_response(response: requests.Response) -> IpstackStandardLookupResponseModel:
        response_as_dictionary = json.loads(response.content.decode("utf-8"))
        return IpstackStandardLookupResponseModel(**response_as_dictionary)
